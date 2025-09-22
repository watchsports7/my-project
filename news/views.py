from django.shortcuts import render, get_object_or_404
from .models import Article, Category


def article_list(request):
    main_article = Article.objects.filter(is_main=True).order_by("-created_at").first()
    articles = Article.objects.order_by("-created_at")
    categories = Category.objects.all()
    return render(request, "news/home.html", {
        "main_article": main_article,
        "articles": articles,
        "categories": categories,
    })


def article_detail(request, slug):
    article = get_object_or_404(Article, slug=slug)
    categories = Category.objects.all()
    related_articles = Article.objects.filter(category=article.category).exclude(id=article.id)[:5]

    return render(request, "news/article_detail.html", {
        "article": article,
        "categories": categories,
        "related_articles": related_articles,
    })


def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    main_article = Article.objects.filter(category=category, is_main=True).order_by("-created_at").first()
    articles = Article.objects.filter(category=category).order_by("-created_at")
    categories = Category.objects.all()

    return render(request, "news/category_detail.html", {
        "category": category,
        "main_article": main_article,
        "articles": articles,
        "categories": categories,
    })


# Страницы "О нас", "Контакты", "Политика конфиденциальности"
def about(request):
    categories = Category.objects.all()
    return render(request, "news/about.html", {"categories": categories})


def contacts(request):
    categories = Category.objects.all()
    return render(request, "news/contacts.html", {"categories": categories})


def privacy(request):
    categories = Category.objects.all()
    return render(request, "news/privacy.html", {"categories": categories})
