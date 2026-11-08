import re
import time
import datetime
import requests
from bs4 import BeautifulSoup as BS

KEYWORDS = ['дизайн', 'фото', 'web', 'python']
PATTERN = re.compile(
    r'\b(?:' + '|'.join(map(re.escape, KEYWORDS)) + r')\b',
    re.IGNORECASE
)

BASE_URL = 'https://habr.com/ru/articles/page{page}/'


def get_soup(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return BS(response.text, 'html.parser')
    except requests.RequestException as e:
        print('Ошибка при загрузке страницы:\n' + str(e))
        return None


def get_topics():
    page = 1
    while True:
        soup = get_soup(BASE_URL.format(page=page))
        if soup is None:
            break

        articles = soup.select('article.tm-articles-list__item')
        if not articles:
            print(f'На странице {page} статьи не найдены — конец ленты.')
            break

        for article in articles:
            title_tag = article.select_one('a.tm-title__link')
            if not title_tag:
                continue

            title = title_tag.get_text(strip=True)
            href = 'https://habr.com' + title_tag['href']

            time_tag = article.find('time')
            date = time_tag['datetime'][:10] if time_tag and time_tag.has_attr('datetime') else 'дата неизвестна'

            preview_text = article.get_text(' ', strip=True).replace('\xa0', ' ')

            if PATTERN.search(preview_text):
                print(f'{date} – {title} – {href}')

        page += 1
        time.sleep(1)


get_topics()
