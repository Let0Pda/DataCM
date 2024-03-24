from pymongo import MongoClient
import json

client = MongoClient("mongodb://localhost:27017/")
db = client["crashes"]
info = db.info

info.delete_many({})  # Удаление всех документов

with open("crash-data.json", "r") as f:
    data = json.load(f)
count_dublicates = 0

for feature in data["features"]:
    _id = feature["properties"]["tamainid"]
    feature["_id"] = _id
    try:
        info.insert_one(feature)
    except Exception:
        count_dublicates += 1
        print(feature)

# TODO update_one(upsert) - можно тоже сделать проверку на дубликаты
print(f"Количество дубликатов: {count_dublicates}")

# count = info.count_documents({})  # Количество документов в коллекции

# for doc in info.find({"properties.tamainid": 48540}):  # Поиск документа
#     print(doc)

# for doc in info.find({"$and": [{"properties.lat2": {"$gt": 35.0, "$lt": 36.0}}, {"properties.vehicle2": "PASSENGER CAR"}]}):
#     print(doc)
