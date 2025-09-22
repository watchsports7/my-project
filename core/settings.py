from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "django-insecure-замени-на-свой"
DEBUG = True

# ⚡ Для разработки можно разрешить все хосты
ALLOWED_HOSTS = ["*"]

# Приложения
INSTALLED_APPS = [
    "jazzmin",  # 🎨 красивый интерфейс админки
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "ckeditor",
    "ckeditor_uploader", # ✅ редактор
    "news",                 # ✅ твое приложение
]

# Куда будут сохраняться загруженные файлы CKEditor
CKEDITOR_UPLOAD_PATH = "uploads/"

CKEDITOR_CONFIGS = {
    "default": {
        "toolbar": "full",
        "height": 400,
        "width": "100%",
    },
}

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],  # глобальная папка для шаблонов
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "news.context_processors.categories",  # категории везде
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"

# База данных (SQLite для разработки)
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Пароли
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Язык и часовой пояс
LANGUAGE_CODE = "ru-ru"
TIME_ZONE = "Europe/Moscow"
USE_I18N = True
USE_TZ = True

# Статика и медиа
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"



DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

JAZZMIN_SETTINGS = {
    "site_title": "InsideSports Admin",  # Заголовок окна браузера
    "site_header": "InsideSports",       # Шапка админки
    "site_brand": "InsideSports",        # Логотип в навбаре
    "site_logo": "img/insidesports-logo.png",                   # Если есть логотип (например 'news/logo.png')
    "welcome_sign": "Добро пожаловать в панель InsideSports",
    "copyright": "InsideSports © 2025",

    # Иконки приложений и моделей
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.User": "fas fa-user",
        "auth.Group": "fas fa-users",
        "news.Article": "far fa-newspaper",
        "news.Category": "fas fa-list",
    },

    # Порядок меню в админке
    "order_with_respect_to": ["news", "auth"],

    # Страницы быстрого доступа
    "topmenu_links": [
        {"name": "Главный сайт", "url": "/", "new_window": True},
        {"app": "news"},  # Автоматически добавляет ссылки для приложения "news"
    ],

    # Пользовательское меню
    "usermenu_links": [
        {"name": "На сайт", "url": "/", "icon": "fas fa-globe"},
        {"model": "auth.user"},
    ],
}
