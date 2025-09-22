from django import forms
from .models import Article

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ["category", "title", "content", "image_url", "is_main"]

    def save(self, commit=True):
        article = super().save(commit=False)
        if commit:
            article.save()
        return article
