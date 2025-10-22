from django import template

register = template.Library()

CATEGORY_COLORS = {
    "football": "bg-success",
    "hockey": "bg-primary",
    "tennis": "bg-warning text-dark",
    "basketball": "bg-danger",
    "foreign": "bg-dark",
}

@register.filter
def category_color(slug):
    """
    Возвращает CSS-класс для бейджа категории.
    """
    return CATEGORY_COLORS.get(slug, "bg-secondary")
