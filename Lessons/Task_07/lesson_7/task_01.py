from selenium import webdriver

# from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

driver = webdriver.Firefox()
driver.get("https://www.amazon.com/")

search_box = driver.find_element(By.ID, "twotabsearchtextbox")
search_box.send_keys("Laptops")
search_box.submit()

assert "Laptops" in driver.title

div_elemtnt = driver.find_element(By.ID, "my-div")
print(div_elemtnt.text)
