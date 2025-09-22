from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("ckeditor/", include("ckeditor_uploader.urls")),  # ✅ для загрузки файлов
    path("", include("news.urls")),
# Статические страницы
    path("about/", TemplateView.as_view(template_name="news/about.html"), name="about"),
    path("contacts/", TemplateView.as_view(template_name="news/contacts.html"), name="contacts"),
    path("privacy/", TemplateView.as_view(template_name="news/privacy.html"), name="privacy"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
