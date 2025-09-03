import io
import os
from urllib.parse import urlparse
import requests
from django.core.files.base import ContentFile
from django.utils import timezone
from slugify import slugify as slugify_ru
from ..models import Article
from .rsport import fetch_lenta_html, parse_lenta, fetch_article_image

def filename_from_url(url: str) -> str:
    path = urlparse(url).path
    name = os.path.basename(path)
    if not name:
        name = "image.jpg"
    return name

def upsert_articles_from_ria(limit: int = 10) -> int:
    """
    Тянет свежие новости, добавляет новые (не дублирует существующие по source_url).
    Возвращает количество добавленных.
    """
    html = fetch_lenta_html()
    items = parse_lenta(html)[:limit]
    added = 0
    for it in items:
        if Article.objects.filter(source_url=it["url"]).exists():
            continue
        title = it["title"]
        slug = slugify_ru(title)

        # Пытаемся достать картинку
        img_url = fetch_article_image(it["url"])
        image_file = None
        if img_url:
            try:
                r = requests.get(img_url, timeout=20)
                r.raise_for_status()
                image_file = ContentFile(r.content, name=filename_from_url(img_url))
            except Exception:
                image_file = None

        article = Article(
            title=title,
            slug=slug,
            source_url=it["url"],
            body="",  # можно дополнительно тянуть лид/абзац — пока пусто
            published_at=timezone.now(),
            is_featured=False,
        )
        if image_file:
            article.image.save(image_file.name, image_file, save=False)
        article.save()
        added += 1
    return added
