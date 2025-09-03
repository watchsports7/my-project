from django.urls import path
from . import views

app_name = 'news'

urlpatterns = [
    path('', views.home, name='home'),
    path('news/<slug:slug>/', views.article_detail, name='detail'),
    path('add/', views.article_create, name='add'),  # ручное добавление
]
