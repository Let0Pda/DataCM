import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from pprint import pprint

ua = UserAgent()

# Запрос веб-страницы
# url = "https://www.boxofficemojo.com/intl/?ref_=bo_nb_hm_tab"
url = "https://www.boxofficemojo.com"

headers = {"User-Agent": ua.chrome}
params = {"ref_": "bo_nb_hm_tab"}

session = requests.session()

response = session.get(f"{url}/intl", params=params, headers=headers)
soup = BeautifulSoup(response.content, "html.parser")
# test_link = soup.find("a", {"class": "a-link-normal"})
rows = soup.find_all("tr")

films = []

for row in rows[2:70]:
    film = {}
    # area_info = row.find("td", {"class": "mojo-field-type-area_id"}).find("a")
    area_info = row.find("td", {"class": "mojo-field-type-area_id"}).findChildren()[0]
    film = {"area": [area_info.text, url + area_info.attrs["href"]]}

    weekend_info = row.find("td", {"class": "mojo-field-type-date_interval"}).findChildren()[0]
    film["weekend"] = [weekend_info.text, url + weekend_info.attrs["href"]]

    film["releases"] = int(row.find("td", {"class": "mojo-field-type-positive_integer"}).text)

    try:
        release_info = row.find("td", {"class": "mojo-field-type-release"}).findChildren()[0]
        film["release"] = [release_info.text, url + release_info.attrs["href"]]
    except Exception:
        print("Exception witch distributor , object = ", film["distributor"])
        film["release"] = None

    try:
        distributor_info = row.find("td", {"class": "mojo-field-type-studio"}).findChildren()[0]
        film["distributor"] = [distributor_info.text, url + distributor_info.attrs["href"]]
    except Exception:
        print("Exception witch release, object = ", film["release"])
        film["distributor"] = None

    film["gross"] = row.find("td", {"class": "mojo-field-type-money"}).text

    films.append(film)
pprint(films)


# for row in rows[2:]:
#     film = {}
#     area_info = row.find("a", {"class": "a-link-normal"})
#     film["area"] = [area_info.text, url + area_info.attrs["href"]]

#     print()
