import scrapy
from scrapy.http import HtmlResponse


class SuperjobruSpider(scrapy.Spider):
    name = "superjobru"
    allowed_domains = ["mo.superjob.ru"]
    start_urls = ["https://mo.superjob.ru/vakansii/rabota-dlya-pensionerov.html"]

    def parse(self, response: HtmlResponse):

        next_page = response.xpath("//a[contains(@class, '-button-dalshe')]/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        links = response.xpath("//div[2]/div/div[1]/div[1]/div/span/a/@href").getall()
        for link in links:
            yield response.follow(link, callback=self.vacancy_parse)

        print()

    def vacancy_parse(self, response: HtmlResponse):
        name = response.xpath("//h1/text()").get()
        salary = response.xpath("//div[1]/div[1]/span/span[1]/text()").getall()
        url = response.url
        url_part = url.split("/")[-1].split(".")[0]
        _id = int(url_part.split("-")[-1])
        yield {"_id": _id, "name": name, "salary": salary, "url": url}

        # print()
