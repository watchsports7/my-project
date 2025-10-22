import os
from django.db import models
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.text import slugify
from django.utils import timezone
from django.utils.html import strip_tags
from taggit.managers import TaggableManager


def safe_image_upload_to(instance, filename):
    """Безопасное сохранение изображений в /media/news/"""
    base, ext = os.path.splitext(filename)
    safe_name = slugify(base)
    return f"news/{safe_name}{ext}"


class Category(models.Model):
    """Категории новостей (Футбол, Хоккей, Девушки и т.д.)"""
    title = models.CharField(max_length=100, verbose_name="Название категории")
    slug = models.SlugField(unique=True, max_length=120, verbose_name="URL категории")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок отображения")

    class Meta:
        ordering = ['order']
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """Автоматическая генерация slug при сохранении."""
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """Ссылка на страницу категории."""
        return reverse('news:category_detail', kwargs={'slug': self.slug})


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="Тег")
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    def __str__(self):
        return self.name


class Article(models.Model):
    """Основная модель новостей"""

    SECTION_CHOICES = [
        ('main', 'Остальные новости'),
        ('foreign', 'Иностранная пресса'),
    ]

    title = models.CharField(max_length=255, verbose_name="Заголовок")
    slug = models.SlugField(unique=True, verbose_name="URL (slug)")
    anons = models.TextField(blank=True, null=True, verbose_name="Анонс")
    content = RichTextUploadingField(verbose_name="Содержание")
    pub_date = models.DateTimeField(default=timezone.now, verbose_name="Дата публикации")

    image = models.ImageField(upload_to=safe_image_upload_to, blank=True, null=True, verbose_name="Изображение (файл)")
    image_url = models.URLField(blank=True, null=True, help_text="Добавьте URL изображения", verbose_name="URL изображения")

    section = models.CharField(max_length=50, choices=SECTION_CHOICES, default='main', verbose_name="Тип публикации")

    views = models.PositiveIntegerField(default=0)

    tags = TaggableManager(blank=True)  # теги

    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, blank=True,
                                     related_name='articles', verbose_name="Раздел спорта")

    telegram_embed = models.TextField(blank=True, null=True, help_text="Код embed из Telegram", verbose_name="Embed из Telegram")
    is_main = models.BooleanField(default=False, verbose_name="Главная новость")

    source_name = models.CharField(max_length=100, blank=True, null=True)  # <-- добавляем
    source_url = models.URLField(blank=True, null=True)  # ссылка на оригинал (по желанию)


    class Meta:
        ordering = ['-pub_date']
        verbose_name = "Новость"
        verbose_name_plural = "Новости"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """Автоматическая генерация slug при сохранении и очистка анонса от HTML."""
        if not self.slug:
            self.slug = slugify(self.title)
        if self.anons:
            self.anons = strip_tags(self.anons).strip()
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """Ссылка на страницу новости"""
        return reverse('news:article_detail', kwargs={'slug': self.slug})


# =======================
# 💬 Модель лайков и дизлайков
# =======================
class ArticleReaction(models.Model):
    """Реакции на новости: лайк / дизлайк с защитой от накрутки по IP"""
    article = models.ForeignKey('Article', on_delete=models.CASCADE, related_name='reactions', verbose_name="Новость")
    ip_address = models.GenericIPAddressField(verbose_name="IP-адрес пользователя")
    is_like = models.BooleanField(verbose_name="Лайк?", help_text="True — лайк, False — дизлайк")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Дата голосования")

    class Meta:
        unique_together = ('article', 'ip_address')  # защита от повторного голосования
        verbose_name = "Реакция на новость"
        verbose_name_plural = "Реакции на новости"

    def __str__(self):
        return f"{'👍' if self.is_like else '👎'} - {self.article.title}"
