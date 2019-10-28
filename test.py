import time
from selenium import webdriver
from bs4 import BeautifulSoup  # pip install bs4
from selenium.webdriver.chrome.options import Options

options = Options()
options.headless = False
driver = webdriver.Chrome('/webdrivers/chromedriver.exe', options=options)
driver.implicitly_wait(10)
driver.set_window_size(1920, 1080)
time.sleep(2)
driver.get("https://www.myscore.com.ua/match/UB2qQlGd/#match-summary")

# navigate to N2N tab
time.sleep(1)
elements = driver.find_element_by_id("li-match-head-2-head")
elements.click()
time.sleep(1)

# return list of matches
# container[0] - home, container[1] - away, container[2] - common
def get_last_matches(count):
    container = driver.find_elements_by_class_name("h2h-wrapper")
    table = container[count].find_element_by_tag_name("tbody")
    last_matches = table.find_elements_by_tag_name("tr")
    return last_matches

# return lengh of last matches
def get_match_list_len(last_matches):
    match_list = []
    for match in last_matches:
        atr = match.get_attribute("class")
        if "highlight" in atr:
            match_list.append(match)
    match_list_len = len(match_list)
    return match_list_len


for count in range(0, 3):
    last_matches = get_last_matches(count)
    list_len = get_match_list_len(last_matches)
    print(list_len)

time.sleep(5)
driver.close()
