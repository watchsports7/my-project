from django.contrib import admin
from django.urls import path, include
from news import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.article_list, name='home'),  # Главная → список статей
    path('news/', include('news.urls')),         # Доп. страницы приложения
]
