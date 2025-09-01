from django.shortcuts import render, get_object_or_404
from .models import Article, Category
from django.http import HttpResponse

def index(request):
    return HttpResponse("Привет! Это главная страница новостей.")

def article_list(request):
    articles = Article.objects.all().order_by('-created_at')  # исправлено
    categories = Category.objects.all()
    return render(request, 'news/article_list.html', {
        'articles': articles,
        'categories': categories,
        'current_category': None
    })


def article_detail(request, pk):
    article = get_object_or_404(Article, pk=pk)
    categories = Category.objects.all()
    return render(request, 'news/article_detail.html', {
        'article': article,
        'categories': categories
    })


def category_articles(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    # исправлено: через related_name="article_set", если явно не задано
    articles = Article.objects.filter(category=category).order_by('-created_at')
    categories = Category.objects.all()
    return render(request, 'news/article_list.html', {
        'articles': articles,
        'categories': categories,
        'current_category': category
    })
