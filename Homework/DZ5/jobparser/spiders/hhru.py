import scrapy
from scrapy.http import HtmlResponse


class HhruSpider(scrapy.Spider):
    name = "hhru"
    allowed_domains = ["hh.ru"]
    start_urls = [
        "https://hh.ru/search/vacancy?from=suggest_post&hhtmFrom=main&hhtmFromLabel=vacancy_search_line&search_field=name&search_field=company_name&search_field=description&text=Python&enable_snippets=false&L_save_area=true"
    ]

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//a[@data-qa='pager-next']/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        links = response.xpath("//span/a[@class='bloko-link' and @target='_blank']/@href").getall()
        for link in links:
            yield response.follow(link, callback=self.vacancy_parse)

    def vacancy_parse(self, response: HtmlResponse):
        name = response.xpath("//h1/text()").get()
        salary_parts = response.xpath("//div[@data-qa='vacancy-salary']//text()").getall()
        salary = self.process_salary_range(salary_parts)
        url = response.url
        yield {"name": name, "salary": salary, "url": url}

    def process_salary_range(self, salary_parts):
        result = ""
        if salary_parts:
            for part in salary_parts:
                cleaned_part = part.replace("\xa0", "").strip()
                if cleaned_part.replace(".", "", 1).isdigit():
                    number = int(cleaned_part.replace(".", "", 1))
                    formatted_number = "{:,}".format(number).replace(",", " ")
                    result += f"{formatted_number} "
                else:
                    result += f"{part} "
        return result.strip()
