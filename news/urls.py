from django.urls import path
from . import views

app_name = "news"

urlpatterns = [
    path("", views.article_list, name="article_list"),
    path("category/<slug:slug>/", views.category_detail, name="category_detail"),
    path("article/<slug:slug>/", views.article_detail, name="article_detail"),

    # 🔹 новые маршруты
    path("about/", views.about, name="about"),
    path("contacts/", views.contacts, name="contacts"),
    path("privacy/", views.privacy, name="privacy"),
]
