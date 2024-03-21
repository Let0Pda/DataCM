import requests
import json

url = "http://openlibrary.org/search.json"

subject = "Artificial intelligence"

params = {"subject": subject, "limit": 10}

response = requests.get(url, params=params)
if response.status_code == 200:
    print(f" Успешный запрос API!")
else:
    print(f"Запрос API отклонен с кодом состояния: {response.status_code}")

data = json.loads(response.text)

books = data["docs"]

for book in books:
    print(f'Title: {book["title"]}')
    print(f'Autor: {book["author_name"]}')
    print(f'Subject: {book["subject"]}')
    print("\n")
