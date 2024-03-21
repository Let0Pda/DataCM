import requests
from bs4 import BeautifulSoup
import json
import re
import pandas as pd

# Инициализация базового URL и счетчика страниц
url = "http://books.toscrape.com/"
current_page_url = f"{url}catalogue/page-1.html"
pages_processed = 0

# Список для хранения информации о книгах
books_data = []

while current_page_url:
    print(f"\nОбрабатывается страница № {pages_processed + 1}")

    # Получение HTML содержимого страницы
    response = requests.get(current_page_url)
    soup = BeautifulSoup(response.text, "html.parser")

    # Поиск всех тегов h3, содержащих информацию о книгах
    book_titles = soup.find_all("h3")

    # Обработка каждой книги на текущей странице
    for title_tag in book_titles:
        # Поиск тега <a> с ссылкой на книгу
        book_link_tag = title_tag.find("a", href=True)
        book_url = f"{url}catalogue/" + book_link_tag["href"]

        # Получение HTML содержимого страницы книги
        book_response = requests.get(book_url)
        book_soup = BeautifulSoup(book_response.text, "html.parser")

        # Извлечение информации о книге
        book_title = book_soup.find("h1").text.strip()
        book_price = float(book_soup.find("p", class_="price_color").text.strip().replace("Â£", ""))
        book_stock = int(re.findall(r"\d+", book_soup.find("p", class_="instock availability").text.strip())[0])
        book_description = book_soup.find("meta", attrs={"name": "description"})["content"]

        # Добавление информации о книге в список
        books_data.append(
            {
                "Название": book_title,
                "Цена": book_price,
                "Количество в наличии": book_stock,
                "Описание": book_description,
            }
        )
        print(f"Добавлена книга: {book_title}")

    # Поиск кнопки "Следующая" для перехода на следующую страницу
    next_page_tag = soup.find("a", string="next")

    # Если есть ссылка на следующую страницу, обновить URL и увеличить счетчик страниц
    if next_page_tag:
        current_page_url = f"{url}catalogue/" + next_page_tag["href"]
        pages_processed += 1
    else:
        current_page_url = None

# Вывод общего количества книг
print(f"\nОбщее количество книг: {len(books_data)}")

# Создание DataFrame из списка словарей
books_df = pd.DataFrame(books_data)

# Вывод первых нескольких строк DataFrame
print(books_df.head())

# Сохранение DataFrame в файл
books_df.to_csv(r"./books_data.toscrape.com.csv")

# Сохранение информации о книгах в файл
with open(r"./books_data.toscrape.com.json", "w", encoding="utf-8") as f:
    json.dump(books_data, f, indent=4, ensure_ascii=False)
