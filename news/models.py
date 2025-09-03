from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Название рубрики")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class Article(models.Model):
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    content = models.TextField(verbose_name="Содержание")
    embed_code = models.TextField(blank=True, null=True, verbose_name="Embed-код (например, Telegram)")
    image = models.ImageField(upload_to="articles/", blank=True, null=True, verbose_name="Изображение")
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата публикации")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="articles", verbose_name="Категория")

    class Meta:
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"
        ordering = ["-pub_date"]

    def __str__(self):
        return self.title
