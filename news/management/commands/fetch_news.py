from django.core.management.base import BaseCommand
from news.services.ingest import fetch_all_news


class Command(BaseCommand):
    help = "Загружает все новости (Р-Спорт, РИА, ТАСС)"

    def handle(self, *args, **options):
        total = fetch_all_news()
        self.stdout.write(self.style.SUCCESS(f"Успешно добавлено {total} новостей"))
