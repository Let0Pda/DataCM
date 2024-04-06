from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import csv

# Инициализация драйвера браузера
driver = webdriver.Chrome()

# Переход на первую страницу веб-сайта
driver.get("http://quotes.toscrape.com/page/1/")
# Инициализация пустого списка для хранения цитат
quotes = []
while True:
    # Поиск всех цитат на странице с помощью xpath
    quote_elements = driver.find_elements(By.XPATH, '//div[@class="quote"]')
    # Извлечение текста каждой цитаты
    for quote_element in quote_elements:
        quote = quote_element.find_element(By.XPATH, './/span[@class="text"]').text
        author = quote_element.find_element(By.XPATH, './/span/small[@class="author"]').text
        quotes.append({"quote": quote, "author": author})
    # Проверка наличия следующей кнопки
    next_button = driver.find_elements(By.XPATH, '//li[@class="next"]/a')
    if not next_button:
        break
    # Нажатие следующей кнопки
    next_button[0].click()
    # Ожидание загрузки страницы
    time.sleep(2)
    # Закрытие браузера
driver.close()

# Вывод цитат
# # в терминал
# for quote in quotes:
#     print(quote["quote"], "by", quote["author"])


# Сохранение цитат в CSV-файл
with open("quotes.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=["quote", "author"])
    writer.writeheader()
    writer.writerows(quotes)
