"""
Загрузите данные который вы получили на предыдущем уроке путем скрейпинга сайта с помощью Buautiful Soup в MongoDB и создайте базу данных и коллекции для их хранения.
"""

from pymongo import MongoClient
import json

json_file = "D:/GitTest/DataC&M/DataCM/Homework/DZ2/books_data.toscrape.com.json"
client = MongoClient("localhost", 27017)
db = client["books_collection"]
data = db.books

# data.delete_many({})  # Удаление всех документов

with open(json_file, "r", encoding="utf-8") as file:
    data_collection = json.load(file)

for item in data_collection:
    data.insert_one(item)
