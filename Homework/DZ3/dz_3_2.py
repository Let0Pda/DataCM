"""
Поэкспериментируйте с различными методами запросов.
"""

from pymongo import MongoClient

client = MongoClient("localhost", 27017)
db = client["books_collection"]
data = db.books


# Количество документов в коллекции
document_count = data.count_documents({})
print(f"Количества документов в коллекции: {document_count}", end="\n\n")

# Запрос количества и названий книг, дороже 55 фунтов
query = {"Цена": {"$gt": 55.0}}
documents = data.find(query)
print(f"Количество книг дороже 55 фунтов - {data.count_documents(query)}", end='\n\n')

for document in documents:
    print(f"Название книги: {document["Название"]}")

# Поиск самой дешевой книги
cheapest_book = data.find_one(sort=[("Цена", 1)])
print(f"\nСамая дешевая книга: {cheapest_book['Название']} - {cheapest_book['Цена']} фунтов", end="\n\n")

# Поиск самой дорогой книги
most_expensive_book = data.find_one(sort=[("Цена", -1)])
print(f"Самая дорогая книга: {most_expensive_book['Название']} - {most_expensive_book['Цена']} фунтов", end="\n\n")

# Поиск книги с минимальным количеством книг в наличии
book_with_min_stock = data.find_one(sort=[("Количество в наличии", 1)])
min_stock = book_with_min_stock['Количество в наличии']
print(f"Минимальное количество книг в наличии: {min_stock} - книга \"{book_with_min_stock['Название']}\"")

# Поиск книги с максимальным количеством книг в наличии
book_with_max_stock = data.find_one(sort=[("Количество в наличии", -1)])
max_stock = book_with_max_stock['Количество в наличии']
print(f"Максимальное количество книг в наличии: {max_stock} - книга \"{book_with_max_stock['Название']}\"")
