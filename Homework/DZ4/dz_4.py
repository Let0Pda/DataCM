import csv
import os
import requests
from lxml import html


current_file_path = os.path.abspath(__file__)  # Получаем путь к текущему файлу
current_directory = os.path.dirname(current_file_path)  # Получаем путь к папке, в которой находится текущий файл
target_directory = os.path.join(current_directory, "data")  # Создаем путь к подпапке, где будет сохранен CSV-файл
os.makedirs(target_directory, exist_ok=True)  # Создаем подпапку, если ее еще не существует
csv_file_path = os.path.join(target_directory, "movies.csv")  # Формируем полный путь к CSV-файлу в подпапке

resp = requests.get(
    url="https://www.imdb.com/chart/moviemeter/?ref_=chtbo_ql_2",
    headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"},
)

tree = html.fromstring(html=resp.content)

movies = tree.xpath("//section/div/div[2]/div/ul/li")
all_movies = []
for movie in movies:
    name = movie.xpath(".//div[2]/div/div/div[2]/a/h3/text()")
    year = movie.xpath(".//div[2]/div/div/div[3]/span[1]/text()")
    rating = movie.xpath(".//div[2]/div/div/span/div/span/text()")
    movie_duration = movie.xpath(".//div[2]/div/div/div[3]/span[2]/text()")
    age_rating = movie.xpath(".//div[2]/div/div/div[3]/span[3]/text()")
    movie_link = movie.xpath(".//div[2]/div/div/div[2]/a/@href")
    movie_url = (f"https://www.imdb.com{movie_link[0]}" if movie_link else "N/A",)

    aria_label_element = movie.xpath(".//div[2]/div/div/div[1]/span")
    if aria_label_element:
        aria_label = aria_label_element[0].get("aria-label")
    else:
        aria_label = "N/A"

    m = {
        "name": name[0] if name else "N/A",
        "year": year[0] if year else "N/A",
        "rating": rating[0] if rating else "N/A",
        "movie_duration": movie_duration[0] if movie_duration else "N/A",
        "age_rating": age_rating[0] if age_rating else "N/A",
        "popularity": aria_label,
        "movie_url": movie_url[0],
    }
    all_movies.append(m)


# Сохраняем данные в CSV-файл в подпапке
with open(csv_file_path, "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=all_movies[0].keys())
    writer.writeheader()
    writer.writerows(all_movies)

print(f"Данные сохранены в файл {csv_file_path}")
