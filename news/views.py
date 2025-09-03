from django.shortcuts import render, get_object_or_404
from .models import Article, Category


def article_list(request):
    articles = Article.objects.all().order_by('-pub_date')
    categories = Category.objects.all()
    return render(request, 'news/article_list.html', {
        'articles': articles,
        'categories': categories,
        'current_category': None
    })


def article_detail(request, pk: int):
    article = get_object_or_404(Article, pk=pk)
    categories = Category.objects.all()
    return render(request, 'news/article_detail.html', {
        'article': article,
        'categories': categories
    })


def category_articles(request, category_id: int):
    category = get_object_or_404(Category, id=category_id)
    articles = category.articles.all().order_by('-pub_date')
    categories = Category.objects.all()
    return render(request, 'news/article_list.html', {
        'articles': articles,
        'categories': categories,
        'current_category': category
    })
