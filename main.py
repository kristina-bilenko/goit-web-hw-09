import json

import requests
from bs4 import BeautifulSoup

quotes_data = []
authors_url_list = []
authors_data = []
page_number = 1

while True:
    url = f'https://quotes.toscrape.com/page/{page_number}/'
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'lxml')

        quotes = soup.find_all('span', class_='text')
        if not quotes:
            break
        authors = soup.find_all('small', class_='author')
        tags = soup.find_all('div', class_='tags')
        quote_blocks = soup.find_all('div', class_='quote')
        for quote_block in quote_blocks:
            author_url = quote_block.find('a', href=True)['href']
            url = f'https://quotes.toscrape.com{author_url}'
            authors_url_list.append(url) if url not in authors_url_list else None

        for i in range(0, len(quotes)):
            tagsforquote = tags[i].find_all('a', class_='tag')
            tags_data = []
            for tagforquote in tagsforquote:
                tags_data.append(tagforquote.text)
            data = {"tags": tags_data, "author": authors[i].text, "quote": quotes[i].text}
            quotes_data.append(data)
        page_number += 1
    else:
        break

with open("quotes.json", "w", encoding="utf-8") as file:
    json.dump(quotes_data, file, ensure_ascii=False, indent=2)


for author_url in authors_url_list:
    response = requests.get(author_url)
    print(author_url, response.status_code)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'lxml')

        fullname = soup.find('h3', class_='author-title')
        born_date = soup.find('span', class_='author-born-date')
        born_location = soup.find('span', class_='author-born-location')
        description = soup.find('div', class_='author-description')

        data = {"fullname": fullname.text, "born_date": born_date.text, "born_location": born_location.text, "description": description.text.replace("\n        ","")}
        authors_data.append(data)


with open("authors.json", "w", encoding="utf-8") as file:
    json.dump(authors_data, file, ensure_ascii=False, indent=2)

