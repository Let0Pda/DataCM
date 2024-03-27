import requests
from lxml import html

resp = requests.get(
    url="https://www.imdb.com/chart/moviemeter/?ref_=chtbo_ql_2",
    headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"},
)

tree = html.fromstring(html=resp.content)

movies = tree.xpath('//ul[@role="presentation"]/li')
all_movies = []
for movie in movies:
    m = {
        "name": movie.xpath(
            './/div[@class="ipc-metadata-list-summary-item__c"]/div/div/div[@class="ipc-title ipc-title--base ipc-title--title ipc-title-link-no-icon ipc-title--on-textPrimary sc-b0691f29-9 klOwFB cli-title"]/a/h3/text()'  # noqa
        ),
        "year": movie.xpath(
            './/div[@class="ipc-metadata-list-summary-item__c"]/div/div/div[@class="sc-b0691f29-7 hrgukm cli-title-metadata"]/span[@class="sc-b0691f29-8 ilsLEX cli-title-metadata-item"]/text()[1]'  # noqa
        )[:-2],
        "rating": movie.xpath('.//div[@class="ipc-metadata-list-summary-item__c"]/div/div/span[@class="sc-b0691f29-1 grHDBY"]/div/span/text()'),
    }
    all_movies.append(m)
print(len(all_movies[:-17]))
print(all_movies[:-17])
