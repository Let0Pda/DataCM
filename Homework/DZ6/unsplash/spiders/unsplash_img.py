import scrapy
from scrapy.http import HtmlResponse
from items import UnsplashItem
from scrapy.loader import ItemLoader


class UnsplashImgSpider(scrapy.Spider):
    name = "unsplash_img"
    allowed_domains = ["unsplash.com"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.start_urls = [f"https://unsplash.com/s/photos/{kwargs.get('query')}"]

    def parse(self, response: HtmlResponse):
        links = response.xpath("//a[@itemprop='contentUrl']")
        for link in links:
            yield response.follow(link, callback=self.parse_photo)

    def parse_photo(self, response: HtmlResponse):
        loader = ItemLoader(item=UnsplashItem(), response=response)
        loader.add_xpath("name", "//h1/text()")
        loader.add_xpath("photos", "//button//img/@srcset")
        loader.add_xpath("description", "//p[@style]/text()")
        loader.add_xpath("date", "//time/@datetime")
        loader.add_value("url", response.url)

        yield loader.load_item()
