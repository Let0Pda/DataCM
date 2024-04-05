# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
# from itemadapter import ItemAdapter

from scrapy.pipelines.images import ImagesPipeline
from scrapy.http import Request
import csv
from pymongo import MongoClient
from pymongo import errors
from datetime import datetime
import uuid
import re

now = datetime.now()
date_string = now.strftime("%d%m%y")
mongo_base_name = f"unsplash{date_string}"


def process_id(item):
    # Генерируем уникальный UUID для item
    return str(uuid.uuid4())


def process_image_info(item):
    # Удаляем "Download this free HD photo of" и все слова, которые предшествуют "of"
    description = re.sub(r"Download this free HD photo of.*?(?=of)", "", item["description"]).strip()
    # Извлекаем название и категорию из item
    name = item["name"]
    category = description.split(",")[0].strip() if "," in description else description
    # Возвращаем словарь с названием, категорией, URL изображения и локальным путем к файлу
    return {"name": name, "category": category, "url": item["photos"][0]["url"], "local_path": item["photos"][0]["path"]}


def save_to_csv(item, spider):
    # Извлекаем информацию об изображении
    image_info = process_image_info(item)
    image_info["_id"] = item["_id"]
    # Открываем CSV-файл в режиме добавления
    with open(f"{spider.name}_{date_string}.csv", "a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["_id", "name", "category", "url", "local_path"])
        # Если файл пустой, записываем заголовки столбцов
        if file.tell() == 0:
            writer.writeheader()
        # Записываем информацию об изображении в CSV-файл
        writer.writerow(image_info)


class UnsplashPipeline:
    def __init__(self, spider):
        self.client = MongoClient("mongodb://localhost:27017/")

    @classmethod
    def from_crawler(cls, crawler):
        return cls(spider=crawler.spider)

    def open_spider(self, spider):
        self.spider = spider

    def process_item(self, item, spider):
        item["_id"] = process_id(item)
        collection = self.client[mongo_base_name][spider.name]
        try:
            collection.insert_one(item)
        except errors.DuplicateKeyError:
            print(f"Ошибка: Документ с _id {item['_id']} уже существует.")
        save_to_csv(item, spider)
        return item

    def close_spider(self, spider):
        self.client.close()


class UnsplashPhotoPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item["photos"]:
            for img in item["photos"]:
                try:
                    yield Request(img)
                except Exception as e:
                    print(e)

    def item_completed(self, results, item, info):
        if results:
            item["photos"] = [itm[1] for itm in results if itm[0]]

        return item
