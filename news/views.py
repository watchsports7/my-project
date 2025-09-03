from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django import forms
from .models import Article

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'body', 'image', 'telegram_embed', 'is_featured']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Заголовок'}),
            'body': forms.Textarea(attrs={'class': 'form-control', 'rows': 6, 'placeholder': 'Текст новости (можно пусто, если Telegram embed)'}),
            'telegram_embed': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Сюда вставь блок Telegram (blockquote + script)'}),
            'is_featured': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

def home(request):
    featured = Article.objects.filter(is_featured=True).order_by('-published_at', '-created_at').first()
    news_list = Article.objects.all().order_by('-published_at', '-created_at')[:50]
    return render(request, 'news/home.html', {'featured': featured, 'news_list': news_list})

def article_detail(request, slug):
    article = get_object_or_404(Article, slug=slug)
    return render(request, 'news/article_detail.html', {'article': article})

def article_create(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            if not article.published_at:
                article.published_at = timezone.now()
            article.save()
            return redirect('news:detail', slug=article.slug)
    else:
        form = ArticleForm()
    return render(request, 'news/article_create.html', {'form': form})
