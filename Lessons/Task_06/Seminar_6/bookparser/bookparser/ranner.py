from scrapy.crawler import CrawlerProcess
from scrapy.utils.reactor import install_reactor
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings

from spiders.book24 import Book24Spider

if __name__ == "__main__":
    install_reactor("twisted.internet.asyncioreactor.AsyncioSelectorReactor")
    configure_logging()
    process = CrawlerProcess(get_project_settings())
    # query = input("Введите тематику для поиска: ")
    process.crawl(Book24Spider, query="Фантастика")
    process.start()
