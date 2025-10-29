from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import F
from django.utils import timezone
from taggit.models import Tag
from .models import Article, Category, ArticleReaction, ArticleView
from django.shortcuts import render
from .models import Article


def get_client_ip(request):
    """Получаем IP-адрес клиента (для защиты от накрутки)."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


# ======= Словарь логотипов (Wikimedia / общедоступные ссылки) =======
# При необходимости дополни/измени ссылки — размер в ссылке (например 120px) можно поменять.
SOURCE_LOGOS = {
    "marca": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/89/Marca_logo.svg/120px-Marca_logo.svg.png",
    "as": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a3/Diario_AS_logo.svg/120px-Diario_AS_logo.svg.png",
    "l'equipe": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/10/L%27%C3%89quipe_logo.svg/120px-L%27%C3%89quipe_logo.svg.png",
    "bild": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/04/Bild_logo.svg/120px-Bild_logo.svg.png",
    "the guardian": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/80/The_Guardian_2018.svg/120px-The_Guardian_2018.svg.png",
    "the sun": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f8/The_Sun.svg/120px-The_Sun.svg.png",
    "daily mail": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/09/Daily_Mail.svg/120px-Daily_Mail.svg.png",
    "bbc sport": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2a/BBC_Sport_2021.svg/120px-BBC_Sport_2021.svg.png",
    "espn": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2f/ESPN_wordmark.svg/120px-ESPN_wordmark.svg.png",
    "sky sports": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/31/Sky_Sports_logo_2017.svg/120px-Sky_Sports_logo_2017.svg.png",
    "gazzetta": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/43/La_Gazzetta_dello_Sport_logo.svg/120px-La_Gazzetta_dello_Sport_logo.svg.png",
    "corriere": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Corriere_dello_Sport_logo.svg/120px-Corriere_dello_Sport_logo.svg.png",
    "sport-express": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6d/Sport-Express_logo.svg/120px-Sport-Express_logo.svg.png",
    "sports.ru": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1c/Sports.ru_logo.svg/120px-Sports.ru_logo.svg.png",
    # добавь сюда свои ссылки по необходимости
}


def resolve_source_logo(source_name: str):
    """
    Попробовать привести source_name к url логотипа:
    - пробует точное совпадение по нижнему регистру,
    - затем частичное совпадение (подстрока).
    Возвращает URL логотипа или None.
    """
    if not source_name:
        return None
    name = source_name.strip().lower()
    # точное совпадение
    if name in SOURCE_LOGOS:
        return SOURCE_LOGOS[name]
    # искать ключ, который является подстрокой в name или наоборот
    for key in SOURCE_LOGOS:
        if key in name or name in key:
            return SOURCE_LOGOS[key]
    return None


def home(request):
    """Главная страница InsideSports с вкладками Главные новости / Иностранная пресса"""

    # Главные новости
    main_articles = Article.objects.filter(is_main=True).order_by('-pub_date')[:9]

    # Иностранная пресса
    foreign_press_articles = list(Article.objects.filter(section='foreign').order_by('-pub_date')[:9])

    # ✅ Добавляем логотип источника (если известен) в каждый объект (атрибут article.source_logo)
    for article in foreign_press_articles:
        # если в модели у тебя есть отдельное поле source_logo (URL), можно приоритетно использовать его:
        if getattr(article, "source_url", None) and getattr(article, "source_name", None):
            # если source_url указывает на страницу, а не на картинку — используем resolve
            # (здесь предполагается, что article.source_logo ещё не сохранён в модели)
            article.source_logo = resolve_source_logo(article.source_name)
        else:
            article.source_logo = resolve_source_logo(getattr(article, "source_name", None))

    # Остальные новости
    other_articles = Article.objects.filter(is_main=False).exclude(section='foreign').order_by('-pub_date')[:12]

    # Боковой блок "Свежие новости"
    latest_articles = Article.objects.order_by('-pub_date')[:10]

    # Словарь цветов для бейджей (ключ — название категории)
    category_colors = {
        'Футбол': 'primary',
        'Хоккей': 'danger',
        'Теннис': 'success',
        'Баскетбол': 'warning text-dark'
    }

    return render(request, 'news/home.html', {
        'main_articles': main_articles,
        'foreign_press_articles': foreign_press_articles,
        'other_articles': other_articles,
        'latest_articles': latest_articles,
        'category_colors': category_colors,
    })


def category_detail(request, slug):
    """Страница категории"""
    category = get_object_or_404(Category, slug=slug)
    articles = Article.objects.filter(category=category).order_by('-pub_date')

    main_article = articles.first()
    other_articles = articles[1:]

    return render(request, 'news/category_detail.html', {
        'category': category,
        'articles': articles,
        'main_article': main_article,
        'other_articles': other_articles,
    })


def article_detail(request, slug):
    """Детальная страница новости"""
    article = get_object_or_404(Article, slug=slug)

    related_articles = Article.objects.filter(
        category=article.category
    ).exclude(id=article.id).order_by('-pub_date')[:5]

    likes_count = article.reactions.filter(is_like=True).count()
    dislikes_count = article.reactions.filter(is_like=False).count()

    ip = get_client_ip(request)
    user_reaction = article.reactions.filter(ip_address=ip).first()

    viewed = ArticleView.objects.filter(article=article, ip_address=ip).exists()

    if not viewed:
        ArticleView.objects.create(article=article, ip_address=ip)
        Article.objects.filter(pk=article.pk).update(views=F('views') + 1)
        article.refresh_from_db(fields=['views'])

    return render(request, 'news/article_detail.html', {
        'article': article,
        'related_articles': related_articles,
        'likes_count': likes_count,
        'dislikes_count': dislikes_count,
        'user_reaction': user_reaction,
    })


@csrf_exempt
def react_article(request, slug):
    """AJAX — обработка лайков и дизлайков"""
    if request.method == 'POST':
        article = get_object_or_404(Article, slug=slug)
        ip = get_client_ip(request)
        action = request.POST.get('action')

        reaction, created = ArticleReaction.objects.get_or_create(
            article=article,
            ip_address=ip,
            defaults={'is_like': (action == 'like'), 'created_at': timezone.now()}
        )

        if not created:
            if action == 'like' and not reaction.is_like:
                reaction.is_like = True
                reaction.save()
            elif action == 'dislike' and reaction.is_like:
                reaction.is_like = False
                reaction.save()

        likes = article.reactions.filter(is_like=True).count()
        dislikes = article.reactions.filter(is_like=False).count()

        return JsonResponse({'likes': likes, 'dislikes': dislikes})

    return JsonResponse({'error': 'Invalid request'}, status=400)


def tag_detail(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    articles = Article.objects.filter(tags=tag).order_by('-pub_date')
    return render(request, 'news/tag_detail.html', {'tag': tag, 'articles': articles})


def rss_feed(request):
    articles = Article.objects.order_by('-pub_date')[:30]
    response = render(request, 'rss/feed.xml', {'articles': articles})
    response['Content-Type'] = 'application/rss+xml; charset=utf-8'
    return response

def about(request):
    return render(request, 'news/about.html')


def contacts(request):
    return render(request, 'news/contacts.html')


def privacy(request):
    return render(request, 'news/privacy.html')
