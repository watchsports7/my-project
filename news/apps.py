from django.apps import AppConfig

class NewsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'news'  # 🔥 обязательно именно так
    verbose_name = 'Новости'
