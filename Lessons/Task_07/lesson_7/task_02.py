from selenium import webdriver
from selenium.webdriver.common.by import By
import time


driver = webdriver.Firefox()
driver.get("https://www.imdb.com/chart/top")
time.sleep(2)
driver.execute_script("window.scrollBy(0, 4000)")
time.sleep(2)
movie_titles_elements = driver.find_elements(By.CSS_SELECTOR, "li.ipc-metadata-list-summary-item h3")
rating_elements = driver.find_elements(By.XPATH, '//span[@class="ipc-rating-star ipc-rating-star--base ipc-rating-star--imdb ratingGroup--imdb-rating"]')

titles = [movie.text for movie in movie_titles_elements]
rating = [movie.text for movie in rating_elements]

for i in range(len(titles)):
    print(f"{titles[i]}: {rating[i]}")

driver.quit()
