# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
# from itemadapter import ItemAdapter
import json
import csv
import re
from datetime import datetime
from pymongo import MongoClient
from pymongo import errors


now = datetime.now()
date_string = now.strftime("%d%m%y")
mongo_base_name = f"vacancies{date_string}"


class JobparserPipeline:

    def __init__(self, spider):
        client = MongoClient("mongodb://localhost:27017/")
        self.spider = spider
        self.mongo_base = client[mongo_base_name]
        self.json_file = open(f"{spider.name}_{date_string}.json", "w", encoding="utf-8")
        self.csv_file = open(f"{spider.name}_{date_string}.csv", "w", newline="", encoding="utf-8")
        self.csv_writer = csv.writer(self.csv_file)
        self.csv_writer.writerow(["_id", "name", "salary", "url"])

    def process_salary(self, item):
        # Заменяем все \xa0 на пробелы и объединяем элементы в строку
        salary_str = " ".join([part.replace("\xa0", " ") for part in item["salary"]])
        # Удаляем лишние пробелы
        salary_value = re.sub(r"\s+", " ", salary_str).strip()
        # Определяем символ валюты
        last_char = salary_str[-1] if salary_str else ""
        currency = "Руб" if last_char == "₽" else last_char
        salary_value = salary_value.replace("₽", "").strip()
        # Формируем единую строку
        item["salary"] = f"{salary_value} {currency}"
        return item

    def process_item(self, item, spider):
        # Обрабатываем поле 'salary'
        item = self.process_salary(item)
        # Вставляем обработанный элемент в базу данных
        collection = self.mongo_base[spider.name]
        try:
            collection.insert_one(item)
        except errors.DuplicateKeyError:
            # Обработка ошибки дублирования ключа
            print(f"Ошибка: Документ с _id {item['_id']} уже существует.")
        # Сохраняем в JSON файл
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.json_file.write(line)
        # Сохраняем в CSV файл
        self.csv_writer.writerow([item["_id"], item["name"], item["salary"], item["url"]])
        # # Выводим обработанный элемент
        # print(item)
        return item

    def close_spider(self, spider):
        # Закрываем файлы после завершения работы паука
        self.json_file.close()
        self.csv_file.close()
