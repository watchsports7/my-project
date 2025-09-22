import re
from django import template

register = template.Library()

@register.filter(name="remove_links")
def remove_links(value):
    """
    Убирает теги <a ...>...</a>, оставляя внутренний текст.
    Сохраняет остальные теги (p, img, strong и т.д.).
    """
    if not value:
        return ""
    # заменяем <a ...>TEXT</a> на TEXT
    return re.sub(r'<a[^>]*>(.*?)</a>', r'\1', value, flags=re.DOTALL)
