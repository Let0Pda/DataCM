from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError  # noqa
from pprint import pprint  # noqa


client = MongoClient("localhost", 27017)
db = client["users"]
# db2 = client['books']
persons = db.persons  # Создание коллекции для документов
duplicate = db.duplicate  # Создание коллекции для дубликатов

"""Добавление документа в коллекцию."""
# doc = {
#     "_id": "00001",
#     "author": "Peter",
#     "age": 38,
#     "text": "is cool! Wildberry",
#     "tags": ["cool", "hot", "ice"],
#     "date": "14.06.1983",
# }


# for doc in persons.find():
#     print()
#     pprint(doc)


"""Множественное добавление документов в коллекцию. И удаление дубликатов"""
# try:
#     persons.insert_one(doc)
# except DuplicateKeyError as e:
#     print(e)

# authors_list = [
#     {"author": "Peter", "age": 38, "text": "is cool", "tags": "cool", "date": "04.08.1971"},
#     {"_id": "123", "author": "Anna", "age": 28, "title": "Hot Cool!!!", "text": "iasy too!", "date": "26.01.1995"},
#     {
#         "author": "Jane",
#         "age": 43,
#         "title": "Nice book",
#         "text": "Pretty text not long",
#         "date": "04.08.1971",
#         "tags": ["fantastic", "criminal"],
#     },
# ]


# for autor in authors_list:
#     try:
#         persons.insert_one(autor)
#     except DuplicateKeyError:
#         duplicate.insert_one(autor)

# persons.insert_many(authors_lost)

# for doc in duplicate.find():
#     pprint(doc)


"""Поисковый запрос"""
# for doc in persons.find({"author": "Peter", "age": 28}):  # Поиск документа - ',' оператор 'и'
#     print(doc)

# # Поиск документа - '$or' оператор 'или' передаются словари
# for doc in persons.find({"$or": [{"author": "Peter"}, {"age": 28}]}):
#     print(doc)

# for doc in persons.find({"age": {"$gt": 30}}):  # Поиск документа - '$gt' оператор 'больше'
#     print(doc)

# for doc in persons.find({"$or": [{"author": "Peter"}, {"age": {"$gt": 20}}]}):  # объединение '$or' и '$gt'
#     print(doc)

# for doc in persons.find({"author": {"$regex": "J."}}):  # регулярное выражение '$regex'
#     print(doc)

# for doc in persons.find({"author": {"$regex": "J."}}, {"_id": 0}):  # регулярное выражение '$regex' с исключением '_id'
#     print(doc)

# for doc in persons.find({"author": {"$regex": "P."}}, {"_id": 0}).sort(
#     "age"
# ):  # подержка сортировки по 'age', можно в обратном потядке '-1'
#     print(doc)

""" Критерии поиска, замена в документе """
# persons.update_one({"author": "Peter"}, {"$set": {"author": "Petya"}})

"""Замена и добавление полей в документе из словаря в документе """

new_data = {"author": "Andrey", "age": 28, "text": "is hot", "date": "11.09.1991"}
# persons.update_one({"author": "Peter"}, {"$set": new_data})

"""Полная замена строки в коллекции"""
# persons.replace_one({"author": "Andrey"}, new_data)


for doc in persons.find():
    print(doc)
