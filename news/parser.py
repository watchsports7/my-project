import requests
from bs4 import BeautifulSoup
from datetime import datetime
from .models import News
from .utils import rewrite_text   # импорт функции рерайта

# URL ленты Риа Спорт
RIA_URL = "https://ria.ru/sport/"

def fetch_main_news():
    """
    Парсит главные новости с ria.ru/sport/
    и сохраняет их в базу.
    """
    response = requests.get(RIA_URL, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(response.text, "html.parser")

    # Берём только первые 5 новостей
    articles = soup.select(".list-item__content")[:5]

    for article in articles:
        # Заголовок
        title = article.select_one(".list-item__title").get_text(strip=True)

        # Ссылка
        link = article.select_one("a")["href"]

        # Проверка: если новость уже есть — пропускаем
        if News.objects.filter(link=link).exists():
            continue

        # Получаем текст статьи
        text = fetch_article_text(link)

        # Делаем рерайт
        rewritten_text = rewrite_text(text)

        # Время публикации (берём текущее)
        pub_date = datetime.now()

        # Картинка
        image_tag = article.select_one("img")
        image_url = image_tag["src"] if image_tag else None

        # Сохраняем в базу
        News.objects.create(
            title=title,
            link=link,
            image=image_url,
            text=rewritten_text,
            pub_date=pub_date
        )

def fetch_article_text(url: str) -> str:
    """
    Достаём текст новости по ссылке
    """
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(response.text, "html.parser")

    # Текст берём из блоков статьи
    paragraphs = soup.select("div.article__text p")
    text = " ".join(p.get_text(strip=True) for p in paragraphs)

    return text
