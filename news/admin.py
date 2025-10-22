from django import forms
from django.contrib import admin
from django.utils.html import format_html, strip_tags as strip_html
from .models import Article, Category, Tag


class ArticleAdminForm(forms.ModelForm):
    """Форма для админки: задаём textarea для анонса и поддерживаем выделение цитат."""

    class Meta:
        model = Article
        fields = '__all__'
        widgets = {
            'anons': forms.Textarea(attrs={'rows': 3, 'cols': 60}),
            'content': forms.Textarea(attrs={
                'rows': 20,
                'cols': 100,
                'style': 'font-family: monospace; font-size: 14px;',
                'placeholder': 'Можно использовать [quote] для выделения цитат.'
            }),
        }

    def clean_anons(self):
        value = self.cleaned_data.get('anons', '') or ''
        return strip_html(value).strip()


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'order')
    list_editable = ('order',)
    search_fields = ('title',)
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    form = ArticleAdminForm

    list_display = ('title', 'category', 'is_main', 'pub_date', 'views', 'source_name')
    list_filter = ('category', 'is_main', 'tags')
    search_fields = ('title', 'content', 'anons', 'source_name')
    list_editable = ('is_main',)
    readonly_fields = ('pub_date', 'preview_image')  # ✅ теперь preview_image здесь
    ordering = ('-pub_date',)
    prepopulated_fields = {'slug': ('title',)}

    fieldsets = (
        ("Основное", {
            'fields': (
                'title',
                'anons',
                'slug',
                'category',
                'tags',
                'section',
                'is_main',
                'pub_date',
                'content',
            ),
        }),
        ("Изображение", {
            'fields': ('image', 'image_url', 'preview_image'),
        }),
        ("Источник (для иностранной прессы)", {
            'fields': ('source_name', 'source_url'),
            'description': 'Укажи название издания (например, Marca, AS, L’Équipe) и ссылку на оригинал.'
        }),
        ("Дополнительно", {
            'fields': ('telegram_embed', 'views'),
        }),
    )

    def preview_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 120px;">', obj.image.url)
        elif obj.image_url:
            return format_html('<img src="{}" style="max-height: 120px;">', obj.image_url)
        return "—"

    preview_image.short_description = "Превью изображения"
