from django.contrib import admin
from django.utils.html import format_html
from .models import Article, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ("name", "slug")
    search_fields = ("name",)


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "is_main", "created_at", "preview_image", "edit_link")
    list_filter = ("category", "is_main", "created_at")
    search_fields = ("title", "content")
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ("created_at", "updated_at", "preview_image", "edit_link")

    fieldsets = (
        ("Основное", {
            "fields": ("title", "slug", "category", "content", "image_url", "telegram_embed", "is_main")
        }),
        ("Служебная информация", {
            "fields": ("created_at", "updated_at", "preview_image", "edit_link"),
        }),
    )

    def preview_image(self, obj):
        """Показывает превью картинки прямо в админке"""
        if obj.image_url:
            return format_html('<img src="{}" style="max-height:150px; border:1px solid #ccc;"/>', obj.image_url)
        return "Нет изображения"
    preview_image.short_description = "Превью"

    def edit_link(self, obj):
        """Ссылка для перехода на страницу новости"""
        return format_html('<a href="/article/{}/" target="_blank">Посмотреть новость</a>', obj.slug)
    edit_link.short_description = "Открыть"
