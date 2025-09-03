import datetime
import re
from typing import List, Optional
import requests
from bs4 import BeautifulSoup
from django.utils import timezone

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; NewsBot/1.0; +https://example.com/bot)"
}

BASE = "https://rsport.ria.ru"

def fetch_lenta_html() -> str:
    url = f"{BASE}/lenta/"
    resp = requests.get(url, headers=HEADERS, timeout=20)
    resp.raise_for_status()
    return resp.text

def parse_lenta(html: str) -> List[dict]:
    """
    Возвращает список коротких записей: title, url (абсолютный), published_at (если найдём).
    """
    soup = BeautifulSoup(html, "lxml")
    items = []
    # На rsport.ria.ru обычно карточки в ссылках с классами типа "list-item__title" и т.п.
    for a in soup.select('a[href^="/"]'):
        href = a.get('href')
        text = (a.get_text() or "").strip()
        if not text or not href:
            continue
        # фильтруем только новости вида /YYYYMMDD/slug.html
        if re.search(r"/\d{8}/", href) and href.endswith(".html"):
            url = BASE + href
            items.append({"title": text, "url": url})
    # Удалим дубликаты по url
    uniq = {}
    for it in items:
        uniq[it["url"]] = it
    return list(uniq.values())

def fetch_article_image(article_url: str) -> Optional[str]:
    try:
        r = requests.get(article_url, headers=HEADERS, timeout=20)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "lxml")
        og = soup.find("meta", attrs={"property": "og:image"})
        if og and og.get("content"):
            return og["content"]
    except Exception:
        return None
    return None

def now_tz():
    return timezone.now()
