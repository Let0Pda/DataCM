# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import MapCompose, TakeFirst, Compose
from datetime import datetime


def proccess_name(name):
    name = name[0].strip()
    return name


def proccess_photos(photos):
    photos = photos.split(",")[-1].split()[0]
    return photos


def process_date(date_dict):
    date_str = date_dict[0]
    date_obj = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%fZ")
    formatted_date = date_obj.strftime("%d-%m-%Y")
    return formatted_date


class UnsplashItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field(input_processor=Compose(proccess_name), output_processor=TakeFirst())
    photos = scrapy.Field(input_processor=MapCompose(proccess_photos))
    description = scrapy.Field(output_processor=TakeFirst())
    date = scrapy.Field(input_processor=Compose(process_date), output_processor=TakeFirst())
    url = scrapy.Field(output_processor=TakeFirst())
    _id = scrapy.Field()
