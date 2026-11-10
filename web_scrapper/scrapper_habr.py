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

BASE_URL = 'https://habr.com/ru/articles/page{page}/' # https://habr.com/ru/articles/page1/ и https://habr.com/ru/articles/ являются равнозначными
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}
TIMEOUT = 15
MAX_PAGES = 50


def get_soup(url):
    try:
        response = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
        response.raise_for_status()
        return BS(response.text, 'html.parser')
    except requests.RequestException as e:
        print(f'Ошибка при загрузке страницы: {e}')
        return None


def get_topics():
    for page in range(1, MAX_PAGES + 1):
        soup = get_soup(BASE_URL.format(page=page))
        if soup is None:
            break

        articles = soup.select('article.tm-articles-list__item')
        if not articles:
            articles = soup.select('article[data-test-id="article"]')
            if not articles:
                print(f'На странице {page} статьи не найдены — конец ленты.')
                break

        for article in articles:
            title_tag = article.select_one('a.tm-title__link')
            if not title_tag:
                title_tag = article.select_one('a[data-test-id="title-link"]')
            if not title_tag:
                continue

            title = title_tag.get_text(strip=True)
            href = 'https://habr.com' + title_tag['href']

            time_tag = article.find('time')
            date = time_tag['datetime'][:10] if time_tag and time_tag.has_attr('datetime') else 'дата неизвестна'

            preview_text = article.get_text(' ', strip=True).replace('\xa0', ' ')

            if PATTERN.search(preview_text):
                print(f'{date} – {title} – {href}')

        time.sleep(1)


if __name__ == '__main__':
    get_topics()