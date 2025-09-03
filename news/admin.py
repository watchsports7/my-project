from django.contrib import admin
from .models import Article

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_featured', 'published_at', 'created_at')
    list_filter = ('is_featured',)
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}
