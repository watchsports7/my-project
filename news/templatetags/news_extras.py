from django import template
from django.utils.html import strip_tags
import re

register = template.Library()


@register.filter(name='category_color')
def category_color(slug):
    """Возвращает CSS-класс бейджа по slug категории."""
    if not slug:
        return 'badge-secondary'

    slug = slug.lower()

    mapping = {
        # Футбол
        'football': 'badge-futbol',
        'futbol': 'badge-futbol',
        'soccer': 'badge-futbol',
        'футбол': 'badge-futbol',

        # Хоккей
        'hockey': 'badge-hockey',
        'hokkej': 'badge-hockey',
        'хоккей': 'badge-hockey',

        # Теннис
        'tennis': 'badge-tennis',
        'теннис': 'badge-tennis',

        # Иностранная пресса
        'foreign': 'badge-foreign',
        'foreign-press': 'badge-foreign',
        'иностранная-пресса': 'badge-foreign',
    }

    return mapping.get(slug, 'badge-secondary')


@register.filter(name='category_color')
def category_color(slug):
    """Возвращает CSS-класс бейджа по slug категории."""
    if not slug:
        return 'badge-secondary'
    mapping = {
        'football': 'badge-futbol',
        'futbol': 'badge-futbol',
        'hokkej': 'badge-hockey',
        'tennis': 'badge-tennis',
        'foreign': 'badge-foreign',
    }
    return mapping.get(slug.lower(), 'badge-secondary')


@register.filter
def dict_get(d, key):
    """Позволяет безопасно брать значение из словаря в шаблоне:
    {{ category_colors|dict_get:article.category.name }}
    """
    try:
        return d.get(key, '')
    except Exception:
        return ''
