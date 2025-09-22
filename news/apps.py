from django.apps import AppConfig


class NewsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "news"

    def ready(self):
        # можно подключить сигналы или сервисы при старте
        pass
