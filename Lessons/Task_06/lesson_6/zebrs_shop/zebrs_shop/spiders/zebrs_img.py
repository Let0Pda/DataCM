import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader import ItemLoader
from ..items import ZebrsShopItem
from itemloaders.processors import MapCompose
from urllib.parse import urljoin


class ZebrsImgSpider(CrawlSpider):
    name = "zebrs_img"
    allowed_domains = ["zebrs.com"]
    start_urls = ["https://www.zebrs.com/categories/smartphones"]

    rules = (
        Rule(LinkExtractor(restrict_xpaths=("//div[@class='position-relative mb-4 teaser-item-div']")), callback="parse_item", follow=True),
        Rule(LinkExtractor(restrict_xpaths=("//a[@rel='next']"))),
    )

    def parse_item(self, response):
        loader = ItemLoader(item=ZebrsShopItem(), response=response)
        loader.default_input_processor = MapCompose(str.strip)

        loader.add_xpath("name", "//h1/text()")

        price_text_danger = response.xpath("//div[@class='me-2 product-price text-danger']/text()").get()

        if price_text_danger:
            loader.add_value("price", price_text_danger)
        else:
            loader.add_value("price", "//div[@class='me-2 product-price']/text()")

        relative_image_urls = response.xpath("//ul[@id='product-zoom']/li/img/@src").getall()
        absolute_image_urls = [urljoin("https://www.zebrs.com", img_url) for img_url in relative_image_urls]
        loader.add_value("image_urls", absolute_image_urls)

        yield loader.load_item()
