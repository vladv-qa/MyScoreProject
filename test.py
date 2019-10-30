import time
from selenium import webdriver
from bs4 import BeautifulSoup  # pip install bs4
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import openpyxl as xl


options = Options()
options.headless = False
driver = webdriver.Chrome('/webdrivers/chromedriver.exe', options=options)
driver.implicitly_wait(10)
driver.set_window_size(1920, 1080)
time.sleep(2)

driver.get("https://www.myscore.com.ua/match/4Mjo1dea/#match-summary")
# navigate to N2N tab
time.sleep(1)


def navigate_to_n2n():
    elements = driver.find_element_by_id("li-match-head-2-head")
    elements.click()
    time.sleep(1)


def get_team_names():
    home_name = driver.find_element_by_class_name('team-text.tname-home').text
    away_name = driver.find_element_by_class_name('team-text.tname-away').text
    print(f"{home_name} ---- {away_name}")
    ...


# return list of matches
# container[0] - home, container[1] - away, container[2] - common
def get_last_matches(container):
    match_list = []
    element = driver.find_elements_by_class_name("h2h-wrapper")
    table = element[container].find_element_by_tag_name("tbody")
    last_matches = table.find_elements_by_tag_name("tr")
    for match in last_matches:
        atr = match.get_attribute("class")
        if "highlight" in atr:
            match_list.append(match)
    return match_list


# limited number of signs
def toFixed(numObj, digits=0):
    return f"{numObj:.{digits}f}"


# return length of last matches
def get_match_list_len(last_matches):
    match_list = []
    for match in last_matches:
        atr = match.get_attribute("class")
        if "highlight" in atr:
            match_list.append(match)
    match_list_len = len(match_list)
    return match_list_len


# print statistics for the last matches (common don't work)
def last_games_statistics(container_number, list_len):
    wins_quantity = 0
    loss_quantity = 0

    last_matches = get_last_matches(container_number)
    for match in last_matches:
        match_result = match.find_element_by_tag_name("a").get_attribute("class")
        if match_result == "form-bg-last form-w":
            wins_quantity = wins_quantity + 1
        elif match_result == "form-bg-last form-l":
            loss_quantity = loss_quantity + 1
    a_draw_quantity = list_len - wins_quantity - loss_quantity
    wins_pers = (wins_quantity / list_len) * 100
    loss_pers = (loss_quantity / list_len) * 100
    a_draw_pers = (a_draw_quantity / list_len) * 100

    print(
        f"Wins - {wins_quantity}/{list_len}, Loss - {loss_quantity}/{list_len}, A Draw - {a_draw_quantity}/{list_len}")
    print(
        f"Wins(%) - {toFixed(wins_pers, 2)}%, Loss (%) - {toFixed(loss_pers, 2)}%, A Draw (%) - {toFixed(a_draw_pers, 2)}%")


# print average goals in the last matches
def goals_statistics(list_of_matches):
    total_goals = 0
    list_len = (len(list_of_matches))
    for item in list_of_matches:
        goals = item.find_element_by_class_name("score").find_element_by_tag_name("strong").get_attribute("innerHTML")
        goals_in_match = sum(list(map(lambda x: int(x.strip()), goals.split(":"))))
        total_goals = total_goals + goals_in_match
    average_goals = (total_goals / list_len)
    print(f"Average goals in the match --> {toFixed(average_goals, 1)}")


# get the result for each url in the list
def get_result(url_list):
    for url in url_list:
        driver.get(url)
        navigate_to_n2n()
        get_team_names()
        # home
        last_matches = get_last_matches(container=0)
        list_len = get_match_list_len(last_matches=last_matches)
        print("Home player statistic:")
        last_games_statistics(container_number=0, list_len=list_len)
        goals_statistics(list_of_matches=last_matches)
        # away
        last_matches = get_last_matches(container=1)
        list_len = get_match_list_len(last_matches=last_matches)
        print("Away player statistic:")
        last_games_statistics(container_number=1, list_len=list_len)
        goals_statistics(list_of_matches=last_matches)


def expand_events(w_driver):
    driver = w_driver
    events = driver.find_elements_by_class_name("event__info")
    for event in events:
        title = event.get_attribute("innerHTML")
        if 'показать игры' in title:
         event.click()


def get_url_list():
    driver.get('https://www.myscore.com.ua')
    expand_events(w_driver=driver)
    url_list = []
    elements = driver.find_elements_by_class_name('event__match.event__match--scheduled.event__match--oneLine')
    for element in elements:
        match_id = element.get_attribute('id').split("_")[-1]
        url = "https://www.myscore.ru/match/{}/#match-summary".format(match_id)
        url_list.append(url)
    return url_list


url_list = get_url_list()

# for item in url_list:
#     print(item)
get_result(url_list=url_list)

time.sleep(5)
driver.close()
