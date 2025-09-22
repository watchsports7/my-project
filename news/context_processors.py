from .models import Category

def categories(request):
    """Делаем список категорий доступным во всех шаблонах"""
    return {"categories": Category.objects.all()}