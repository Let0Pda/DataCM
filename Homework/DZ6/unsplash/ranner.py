from scrapy.crawler import CrawlerProcess
from scrapy.utils.reactor import install_reactor
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
from spiders.unsplash_img import UnsplashImgSpider

query = "Ромашки"
# query = input("Введите тематику для поиска изображений: ")
if __name__ == "__main__":
    install_reactor("twisted.internet.asyncioreactor.AsyncioSelectorReactor")
    configure_logging()
    process = CrawlerProcess(get_project_settings())
    process.crawl(UnsplashImgSpider, query=query)
    process.start()
