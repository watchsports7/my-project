from django.urls import path
from . import views
from .feeds import LatestArticlesFeed

app_name = 'news'

urlpatterns = [
    path('', views.home, name='home'),
    path('category/<slug:slug>/', views.category_detail, name='category_detail'),
    path('article/<slug:slug>/', views.article_detail, name='article_detail'),
    path('about/', views.about, name='about'),
    path('contacts/', views.contacts, name='contacts'),
    path('privacy/', views.privacy, name='privacy'),
    path('tag/<slug:slug>/', views.tag_detail, name='tag_detail'),
    path('article/<slug:slug>/react/', views.react_article, name='react_article'),
    path('rss/', views.rss_feed, name='rss_feed')
]
