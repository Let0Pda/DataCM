import scrapy


class CountriesSpider(scrapy.Spider):
    name = "countries"
    allowed_domains = ["tradingeconomics.com"]
    start_urls = ["https://tradingeconomics.com/country-list/inflation-rate?continent=world"]

    def parse(self, response):
        countries = response.xpath("//td/a")

        for country in countries:
            name = country.xpath(".//text()").get()
            link = country.xpath(".//@href").get()

            if name and link:
                yield response.follow(url=link, callback=self.parse_country, meta={"country_name": name.strip()})

    def parse_country(self, response):
        name = response.meta["country_name"]
        rows = response.xpath("//tr[contains(@class, 'datatable')]")

        for row in rows:
            related = row.xpath(".//td/a/text()").get()
            last = row.xpath(".//td[2]/text()").get()
            previous = row.xpath(".//td[3]/text()").get()

            if related and last and previous:
                try:
                    last = float(last.strip())
                    previous = float(previous.strip())
                    yield {"country_name": name, "related": related.strip(), "last": last, "previous": previous}
                except ValueError:
                    self.logger.warning(f"Could not convert to float: {last} or {previous}")
