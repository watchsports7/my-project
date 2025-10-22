from django import template
from datetime import datetime

register = template.Library()

MONTHS_RU = {
    1: "января",
    2: "февраля",
    3: "марта",
    4: "апреля",
    5: "мая",
    6: "июня",
    7: "июля",
    8: "августа",
    9: "сентября",
    10: "октября",
    11: "ноября",
    12: "декабря",
}

@register.filter
def ru_date(value):
    """Преобразует дату в формат: 10 октября 2025, 16:22"""
    if not isinstance(value, datetime):
        return value
    month = MONTHS_RU.get(value.month, "")
    return f"{value.day} {month} {value.year}, {value.strftime('%H:%M')}"
