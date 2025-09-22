import requests
import xml.etree.ElementTree as ET
from django.utils.text import slugify
from news.models import Article, Category
from datetime import datetime


def fetch_rsport_news():
    url = "https://rsport.ria.ru/export/rss2/archive/index.xml"
    response = requests.get(url)
    response.raise_for_status()

    root = ET.fromstring(response.content)

    category, _ = Category.objects.get_or_create(
        slug="football",
        defaults={"name": "Футбол"}
    )

    added = 0
    for item in root.findall("./channel/item"):
        title = item.find("title").text
        link = item.find("link").text
        pub_date = item.find("pubDate").text
        description = item.find("description").text if item.find("description") is not None else ""

        try:
            published_at = datetime.strptime(pub_date, "%a, %d %b %Y %H:%M:%S %z")
        except Exception:
            published_at = datetime.now()

        slug = slugify(title)[:50]

        _, created = Article.objects.get_or_create(
            slug=slug,
            defaults={
                "title": title,
                "text": description,
                "image_url": None,
                "published_at": published_at,
                "category": category,
                "source_url": link,
            }
        )
        if created:
            added += 1

    print(f"Добавлено {added} новостей с Р-Спорт")
    return added
