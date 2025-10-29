from django.contrib.syndication.views import Feed
from django.utils.html import strip_tags
from django.utils.feedgenerator import Rss201rev2Feed
from .models import Article
from django.utils import timezone
from email.utils import format_datetime

class LatestArticlesFeed(Feed):
    title = "InsideSports — свежие спортивные новости"
    link = "https://inside-sports.ru/"
    description = "Последние статьи о футболе, хоккее, теннисе и других видах спорта"
    feed_type = Rss201rev2Feed

    def items(self):
        return Article.objects.order_by('-pub_date')[:30]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        # если у статьи есть анонс — используем его, иначе контент
        return strip_tags(item.anons or item.content)[:400]

    def item_link(self, item):
        return f"https://inside-sports.ru/article/{item.slug}/"

    def item_pubdate(self, item):
        pub_date = item.pub_date
        if timezone.is_naive(pub_date):
            pub_date = timezone.make_aware(pub_date)
        # Принудительно форматируем дату в RFC 822 (английский)
        return format_datetime(pub_date)
