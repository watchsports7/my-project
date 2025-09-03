from django.apps import AppConfig
import os

class NewsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'news'

    def ready(self):
        # Запускаем планировщик только в режиме сервера (не во время миграций/collectstatic и т.п.)
        if os.environ.get("RUN_MAIN") != "true":
            return
        from apscheduler.schedulers.background import BackgroundScheduler
        from apscheduler.triggers.interval import IntervalTrigger
        from .services.ingest import upsert_articles_from_ria

        scheduler = BackgroundScheduler(timezone="Europe/Moscow")

        def job():
            try:
                upsert_articles_from_ria(limit=12)
            except Exception as e:
                print("[APScheduler] Ingest error:", e)

        # каждые 10 минут
        scheduler.add_job(job, IntervalTrigger(minutes=10), id="ria_ingest", replace_existing=True)
        scheduler.start()
