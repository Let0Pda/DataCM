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
        self.client = MongoClient("mongodb://localhost:27017/")

    @classmethod
    def from_crawler(cls, crawler):
        return cls(spider=crawler.spider)

    def open_spider(self, spider):
        self.items = []  # Инициализируем список для хранения элементов

        self.csv_file = open(f"{spider.name}_{date_string}.csv", "a", newline="", encoding="utf-8")
        self.csv_writer = csv.writer(self.csv_file)
        self.csv_writer.writerow(["_id", "name", "salary", "url"])

    def process_salary(self, item):
        # Заменяем все \xa0 на пробелы и объединяем элементы в строку
        salary_str = " ".join([part.replace("\xa0", " ") for part in item["salary"]])
        # Регулярное выражение для поиска числовых значений зарплаты
        salary_pattern = re.compile(r"\d+(?:\s*\d+)*")
        # Регулярное выражение для поиска символа валюты
        currency_pattern = re.compile(r"[₽$€]")
        # Ищем числовые значения зарплаты
        salary_values = salary_pattern.findall(salary_str)
        # Объединяем найденные числовые значения в строку
        salary_value = " - ".join(salary_values)
        # Ищем символ валюты
        currency_match = currency_pattern.search(salary_str)
        currency_symbol = currency_match[0] if currency_match else None
        # Заменяем символ валюты на текстовое представление
        currency_dict = {"₽": "Руб", "$": "Доллар", "€": "Евро"}
        currency = currency_dict.get(currency_symbol, "Не указано")
        # Формируем единую строку с зарплатой и валютой
        item["salary"] = f"{salary_value} {currency}"
        return item

    def process_item(self, item, spider):
        # Обрабатываем поле 'salary'
        item = self.process_salary(item)
        self.items.append(item)
        # Вставляем обработанный элемент в базу данных
        collection = self.client[mongo_base_name][spider.name]
        try:
            collection.insert_one(item)
        except errors.DuplicateKeyError:
            # Обработка ошибки дублирования ключа
            print(f"Ошибка: Документ с _id {item['_id']} уже существует.")
        # # Сохраняем в JSON файл
        # line = json.dumps(dict(item), ensure_ascii=False) + "," + "\n"
        # self.json_file.write(line)
        # Сохраняем в CSV файл
        self.csv_writer.writerow([item["_id"], item["name"], item["salary"], item["url"]])
        return item

    def close_spider(self, spider):
        # Записываем все элементы из списка в файл JSON
        with open(f"{spider.name}_{date_string}.json", "w", encoding="utf-8") as json_file:
            json.dump(self.items, json_file, ensure_ascii=False, indent=4, separators=(", ", ": "))

        self.csv_file.close()
        self.client.close()
