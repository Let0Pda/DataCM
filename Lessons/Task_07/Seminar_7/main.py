from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

import time

options = Options()
options.add_argument("start-maximized")
driver = webdriver.Chrome(options=options)

driver.get("https://www.wildberries.ru/")

# input = driver.find_element(By.XPATH, "//input[@id='searchInput']")
time.sleep(2)
cookies = driver.find_element(By.XPATH, "//button[@data-link='{on ok}']")
cookies.send_keys(Keys.ENTER)

time.sleep(1)
my_input = driver.find_element(By.ID, "searchInput")
my_input.send_keys("телевизор")
my_input.send_keys(Keys.ENTER)

time.sleep(1)
while True:

    while True:
        wait = WebDriverWait(driver, 30)
        cards = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//article[@id]")))  # через объект ожидания

        # cards = driver.find_elements(By.XPATH, "//article[@id]")  # 100
        # print(len(cards))
        count = len(cards)
        driver.execute_script("window.scrollBy(0,2000)")
        time.sleep(2)
        cards = driver.find_elements(By.XPATH, "//article[@id]")
        if len(cards) == count:
            break

    for card in cards:
        price = card.find_element(By.XPATH, './/ins[contains(@class, "price__lower-price")]').text
        # price = int(price.replace(" ", "").replace("₽", "").replace("&nbsp", "."))
        name = card.find_element(By.XPATH, "./div/a").get_attribute("aria-label")
        url = card.find_element(By.XPATH, "./div/a").get_attribute("href")
        # print(card) # дальше сохраняем и обрабатываем объект //h1[@class="not-found-search__title"]

        print(name, price, url)

    try:
        button = driver.find_element(By.CLASS_NAME, "pagination-next")
        actions = ActionChains(driver)
        actions.move_to_element(button).click()
        actions.perform()

    except Exception:
        break

print()
