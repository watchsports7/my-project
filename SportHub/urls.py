from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from django.contrib.sitemaps import GenericSitemap, Sitemap
from django.contrib.syndication.views import Feed
from django.urls import reverse
from news.models import Article, Category


# --- Sitemap для статических страниц ---
class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'monthly'

    def items(self):
        return ['news:about', 'news:contacts', 'news:privacy']

    def location(self, item):
        return reverse(item)


# --- Sitemap для статей ---
article_info = {
    'queryset': Article.objects.all(),
    'date_field': 'pub_date',
}

# --- Sitemap для категорий ---
category_info = {
    'queryset': Category.objects.all(),
    'date_field': None,
}

# --- Объединённый sitemap ---
sitemaps = {
    'articles': GenericSitemap(article_info, priority=0.9),
    'categories': GenericSitemap(category_info, priority=0.7),
    'static': StaticViewSitemap,
}


# --- RSS-лента ---
class LatestArticlesFeed(Feed):
    title = "InsideSports — последние новости спорта"
    link = "/rss.xml"
    description = "Свежие материалы сайта InsideSports по футболу, хоккею, теннису и другим видам спорта."

    def items(self):
        return Article.objects.order_by('-pub_date')[:20]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.anons or (item.content[:200] + '...')

    def item_link(self, item):
        return reverse('news:article_detail', args=[item.slug])

    def item_pubdate(self, item):
        return item.pub_date


urlpatterns = [
    path("admin/", admin.site.urls),
    path("i18n/", include("django.conf.urls.i18n")),  # если джазмин или языки
    path("ckeditor/", include("ckeditor_uploader.urls")),
    path("", include("news.urls", namespace="news")),

    # --- Sitemap ---
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),

    # --- RSS ---
    path('rss.xml', LatestArticlesFeed(), name='rss_feed'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
