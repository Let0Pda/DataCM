from selenium import webdriver
from selenium.webdriver.common.by import By
import csv

# Инициализация драйвера
driver = webdriver.Chrome()


# Переход на веб-сайт DuckDuckGo
driver.get("https://duckduckgo.com/")

# Поиск строки поиска и ввод поискового запроса
search_bar = driver.find_element(By.NAME, "q")
search_bar.send_keys("Selenium books")

# Поиск кнопки поиска и нажатие на нее
search_button = driver.find_element(By.XPATH, '//button[@type="submit"]')
search_button.click()

# Поиск выпадающего меню "Время" и щелчок по нему
time_dropdown = driver.find_element(By.XPATH, "//*[@id='links_wrapper']/div[1]/div[1]/div/div[3]/a")
time_dropdown.click()

# Поиск опции "За последний месяц" в выпадающем меню времени и щелчок по ней
time_last_month = driver.find_element(By.XPATH, "*//a[@data-value='m']")
time_last_month.click()

# Поиск кнопки "Еще" и щелчок по ней
more_btn = driver.find_element(By.XPATH, '//button[@id="more-results"]')
more_btn.click()

# Поиск всех результатов на странице
results = driver.find_elements(By.XPATH, '//article[@data-nrn="result"]')
result_data = []

# Извлечение заголовка и URL каждого результата
for result in results:
    result_title = result.find_element(By.XPATH, './/a[@data-testid="result-title-a"]/span').text
    result_url = result.find_element(By.XPATH, './/a[@data-testid="result-extras-url-link"]').get_attribute("href")
    result_data.append([result_title, result_url])
driver.quit()

# Запись данных в файл CSV
with open("duckduckgo_results.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Result Title", "URL"])
    writer.writerows(result_data)
