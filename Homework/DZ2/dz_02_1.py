import requests
from bs4 import BeautifulSoup
import json
import re
import pandas as pd


def extract_book_details(book_url):
    """Extracts book details from a given book URL."""
    try:
        response = requests.get(book_url)
        response.raise_for_status()  # Raise an exception for error status codes

        soup = BeautifulSoup(response.text, "html.parser")

        title = soup.find("h1").text.strip()
        price_text = soup.find("p", class_="price_color").text.strip()
        price = float(re.findall(r"\d+\.\d+", price_text)[0])  # Extract numeric price
        stock = int(re.findall(r"\d+", soup.find("p", class_="instock availability").text.strip())[0])
        description = soup.find("meta", attrs={"name": "description"})["content"]

        return {
            "Название": title,
            "Цена": price,
            "Количество в наличии": stock,
            "Описание": description,
        }
    except requests.exceptions.RequestException as e:
        print(f"Error fetching book details: {e}")
        return None


def scrape_category_page(category_url):
    """Scrapes book data from a category page and its subsequent pages."""
    books_data = []
    while category_url:
        print(f"\nОбрабатывается страница: {category_url}")
        response = requests.get(category_url)
        soup = BeautifulSoup(response.text, "html.parser")

        for book_link_tag in soup.find_all("a", href=True):
            if book_link_tag["href"].startswith("/catalogue/"):
                book_url = f"http://books.toscrape.com/catalogue/{book_link_tag['href']}"
                book_data = extract_book_details(book_url)
                if book_data:
                    books_data.append(book_data)

        next_page_tag = soup.find("a", string="next")
        category_url = f"http://books.toscrape.com/catalogue/{next_page_tag['href']}" if next_page_tag else None

    return books_data


def main():
    """Main function to scrape data and save it."""
    base_url = "http://books.toscrape.com/"
    all_books = []

    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, "html.parser")

    for category_link in soup.find("ul", class_="nav nav-list").find_all("a", href=True):
        if category_link["href"].startswith("/catalogue/category/books/"):
            category_url = base_url + category_link["href"]
            category_books = scrape_category_page(category_url)
            all_books.extend(category_books)

    print(f"\nОбщее количество книг: {len(all_books)}")

    books_df = pd.DataFrame(all_books)
    print(books_df.head())

    books_df.to_csv(r"./books_data.toscrape.com.csv")

    with open(r"./books_data.toscrape.com.json", "w", encoding="utf-8") as f:
        json.dump(all_books, f, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    main()
