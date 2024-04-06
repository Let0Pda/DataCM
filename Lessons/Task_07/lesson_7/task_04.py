from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# открытие браузера
driver = webdriver.Chrome()


driver.get("https://quotes.toscrape.com/page/1/")
# ожидание загрузки элемента
wait = WebDriverWait(driver, 10)
element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".quote")))
# извлечение данных из элемента
quote = element.text
driver.quit()
print(quote)
