from .models import Category

def categories_processor(request):
    """Доступ к категориям во всех шаблонах (отсортированы по created_at: newest first)."""
    return {"categories": Category.objects.all()}