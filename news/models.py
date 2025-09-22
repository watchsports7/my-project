from django.contrib import admin
from django.db import models
from ckeditor.widgets import CKEditorWidget
from django.contrib.auth import get_user_model
from ckeditor.fields import RichTextField

class ArticleAdmin(admin.ModelAdmin):
    ...
    formfield_overrides = {
        models.TextField: {'widget': CKEditorWidget()},
    }

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Название категории")
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class Article(models.Model):
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    category = models.ForeignKey(Category, related_name="articles", on_delete=models.CASCADE, verbose_name="Категория")
    content = RichTextField (verbose_name="Текст статьи")
    image_url = models.URLField(blank=True, null=True, verbose_name="Картинка (URL)")
    telegram_embed = models.TextField(blank=True, null=True, verbose_name="Embed из Telegram")
    is_main = models.BooleanField(default=False, verbose_name="Главная новость")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    User = get_user_model()
