# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
# from itemadapter import ItemAdapter
from ranner import query
from scrapy.pipelines.images import ImagesPipeline
from scrapy.http import Request
import csv
from pymongo import MongoClient, errors
from datetime import datetime
import uuid
import re


now = datetime.now()
date_string = now.strftime("%d%m%y")
mongo_base_name = f"unsplash{date_string}"
request_img = query


def process_id(item):
    # Генерируем уникальный UUID для item
    return str(uuid.uuid4())


def process_description(description):
    # Извлечение автора из описания
    author_match = re.search(r"by\s(.+)", description)
    if author_match:
        author = author_match.group(1)
        # Удаление автора из описания
        description = re.sub(r"by\s(.+)", "", description)
    else:
        author = None

    # Удаление "Download this free HD photo of" и текста до "of"
    filtered_description = re.sub(r"^.*?of\s+", "", description).strip()

    return filtered_description, author


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
        item["description"], item["author"] = process_description(item["description"])

        # Сохранение в MongoDB
        collection = self.client[mongo_base_name][request_img]
        try:
            collection.insert_one(item)
        except errors.DuplicateKeyError:
            print(f"Ошибка: Документ с _id {item['_id']} уже существует.")
        print()
        # Сохранение в CSV
        self.save_to_csv(item)

        return item

    def close_spider(self, spider):
        self.client.close()

    def save_to_csv(self, item):
        # Определение пути к CSV файлу
        csv_file_path = f"{request_img}_{date_string}.csv"

        # Определение полей на основе содержания элемента item
        fieldnames = list(item.keys())

        # Проверяем наличие CSV файла и записываем данные
        with open(csv_file_path, mode="a+", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            if file.tell() == 0:  # Проверка на пустой файл
                writer.writeheader()
            writer.writerow(item)


class UnsplashPhotoPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        if item["photos"]:
            for img in item["photos"]:
                try:
                    yield Request(img, meta={"image_name": request_img})
                except Exception as e:
                    print(e)

    def file_path(self, request, response=None, info=None, *, item=None):
        return f'{request.meta["image_name"]}/{super().file_path(request, response=response, info=info)}'

    def item_completed(self, results, item, info):
        if results:
            item["photos"] = [itm[1] for itm in results if itm[0]]
        print()
        return item
