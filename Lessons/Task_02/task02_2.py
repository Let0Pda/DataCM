# sourcery skip: merge-dict-assign, move-assign-in-block
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from pprint import pprint

ua = UserAgent()

# url = "https://gb.ru/posts"
url = "https://gb.ru"

headers = {"User-Agent": ua.chrome}
params = {"page": 1}

session = requests.session()


all_posts = []

while True:
    response = session.get(f"{url}/posts", headers=headers, params=params)
    soup = BeautifulSoup(response.content, "html.parser")

    posts = soup.find_all("div", {"class": "text-left v-padder m-r m-l"})
    if not posts:  # 0 0.0 '' [] () None False,  когда список пустой
        break

    for post in posts:
        post_info = {}

        name_info = post.find("a", {"class": "post-item__title"})
        post_info["name"] = name_info.text
        post_info["url"] = url + name_info.attrs["href"]
        post_info["publication"] = post.find("div", {"class": "small m-t-xs"}).text

        add_info = post.find("div", {"class": "text-muted"}).findChildren("span")
        post_info["views"] = int(add_info[0].text)
        post_info["comments"] = int(add_info[1].text)

        all_posts.append(post_info)
    print(f"Обработана {params['page']} страница")
    params["page"] += 1

pprint(all_posts)
pprint(f"Всего {len(all_posts)} публикаций на сервере.")
