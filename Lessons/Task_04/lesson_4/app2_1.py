import requests
from lxml import html
from pymongo import MongoClient


def get_movies(list_movies):

    client = MongoClient("mongodb://localhost:27017/")
    db = client["imdb_movies"]
    collection = db["top_movies"]
    collection.delete_many({})
    collection.insert_many(list_movies)
    client.close()


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


if __name__ == "__main__":
    get_movies(all_movies)
    # print(all_movies)
