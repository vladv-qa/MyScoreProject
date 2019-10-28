import time
from selenium import webdriver
from bs4 import BeautifulSoup  # pip install bs4
from selenium.webdriver.chrome.options import Options

def sound_off(driver):
    sound_switch = driver.find_element_by_id("sound-switch")
    atr = sound_switch.get_attribute("class")
    time.sleep(10)
    if atr == "ifmenu-sound-link soundTab":
        sound_switch.click()

def expand_events(w_driver):
    driver = w_driver
    events = driver.find_elements_by_class_name("event__info")
    for event in events:
        title = event.get_attribute("title")
        if title == "Показать все игры этого турнира!":
            event.click()


def track_matches(html):
    soup = BeautifulSoup(html, "html.parser")
    elements = soup.select(".event__match.event__match--live.event__match--oneLine")
    for element in elements:
        time_match = element.select_one("div.event__stage")
        goals = element.select_one("div.event__scores.fontBold")
        id_match = element["id"].split("_")[-1]
        partipiciant_nome = element.select_one("div.event__participant.event__participant--home").text
        partipiciant_away = element.select_one("div.event__participant.event__participant--away").text

        if time_match and goals:
            time_match = time_match.text.strip()
            goals = goals.text.strip()
            if time_match.isdigit():
                time_match = int(time_match)
                total_goals = sum(list(map(lambda x: int(x.strip()), goals.split("-"))))
                urls = "https://www.myscore.ru/match/{}/#match-summary".format(id_match)
                if time_match > 15 and total_goals < 2:
                    print(
                        f"{time_match} min | Кількість голів - {total_goals} | {partipiciant_nome} {goals} {partipiciant_away} : {urls}")


options = Options()
options.headless = False
driver = webdriver.Chrome('/webdrivers/chromedriver.exe', options=options)
driver.implicitly_wait(10)
driver.set_window_size(1920, 1080)
time.sleep(2)
driver.get("https://www.myscore.ru/")

time.sleep(2)
elements = driver.find_elements_by_css_selector("div.tabs__tab")
elements[1].click()


temp_hash = 0
while True:
    html = driver.find_element_by_css_selector("div[id=live-table]").get_attribute("innerHTML")
    expand_events(driver)
    sound_off(driver)
    if temp_hash != hash(html):
        track_matches(html)
        temp_hash = hash(html)
    print("----------||----------")
    time.sleep(2)
