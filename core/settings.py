# ruff: noqa: ERA001, E501
"""Base settings to build other settings files upon."""
import datetime
import os
from pathlib import Path

from decouple import config
from django.utils.translation import gettext_lazy as _

from core.read_envs import env

SECRET_KEY = config('SECRET_KEY')

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent.parent
APPS_DIR = BASE_DIR / "apps"

ALLOWED_HOSTS = [config("ALLOW_HOSTS")]

# GENERAL
# ------------------------------------------------------------------------------
DEBUG = config("DEBUG", cast=bool, default=False)
TIME_ZONE = "UTC"
LANGUAGE_CODE = "en"

LANGUAGES = [
    ("en", _("English")),
    ("fa", _("Farsi")),
]
SITE_ID = 1
USE_I18N = True
USE_TZ = True
LOCALE_PATHS = [str(BASE_DIR / "locale")]

# DATABASES
# ------------------------------------------------------------------------------
DATABASES = {"default": env.db("DATABASE_URL")}
DATABASES["default"]["ATOMIC_REQUESTS"] = True
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# URLS
# ------------------------------------------------------------------------------
ROOT_URLCONF = "core.urls"
WSGI_APPLICATION = "core.wsgi.application"

# APPS
# ------------------------------------------------------------------------------
DJANGO_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.admin",
    "django.forms",
]
THIRD_PARTY_APPS = [
    "django_celery_beat",
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_simplejwt',
    "django_celery_results",
    "corsheaders",
    "rolepermissions",
    "drf_yasg",
    "django_filters",
]

LOCAL_APPS = [
    "apps.base",
    "apps.profiles",
    "apps.account",
    "apps.chatroom",
    "apps.sms",
]
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# AUTHENTICATION
# ------------------------------------------------------------------------------
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
]

AUTH_USER_MODEL = "profiles.User"
ROLEPERMISSIONS_REGISTER_ADMIN = False
ROLEPERMISSIONS_SUPERUSER_SUPERPOWERS = False
ROLEPERMISSIONS_MODULE = 'tools.project.common.roles'

# LOGIN_REDIRECT_URL = "users:redirect"
# LOGIN_URL = "account_login"

# PASSWORDS
# ------------------------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# MIDDLEWARE
# ------------------------------------------------------------------------------
DJANGO_MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

THIRD_PARTY_MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
]

MIDDLEWARE = DJANGO_MIDDLEWARE + THIRD_PARTY_MIDDLEWARE

# STATIC
# ------------------------------------------------------------------------------
STATIC_URL = "static/"
STATIC_ROOT = os.path.join(BASE_DIR, "social_network", "staticfiles")

# MEDIA
# ------------------------------------------------------------------------------
MEDIA_ROOT = os.path.join(BASE_DIR, "social_network", "media")
MEDIA_URL = "/media/"
IMAGE_URL_SERVE = config("IMAGE_URL_SERVE")

# TEMPLATES
# ------------------------------------------------------------------------------
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [str(BASE_DIR / "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

FORM_RENDERER = "django.forms.renderers.TemplatesSetting"

# ADMIN
# ------------------------------------------------------------------------------
# Django Admin URL.
ADMIN_URL = "admin/"

# LOGGING
# ------------------------------------------------------------------------------
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s",
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "root": {"level": "INFO", "handlers": ["console"]},
}

# CORS
# -------------------------------------------------------------------------------
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = (
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
    "source",
    "appname",
    "appversion",
    "API-Version",
    "APP-Version",
)

# Celery
# ------------------------------------------------------------------------------
if USE_TZ:
    CELERY_TIMEZONE = TIME_ZONE
CELERY_BROKER_URL = config("CELERY_BROKER_URL")
CELERY_RESULT_BACKEND = "django-db"
CELERY_RESULT_EXTENDED = True
CELERY_RESULT_BACKEND_ALWAYS_RETRY = True
CELERY_RESULT_BACKEND_MAX_RETRIES = 10
CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TASK_TIME_LIMIT = 5 * 60
CELERY_TASK_SOFT_TIME_LIMIT = 60
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"
CELERY_WORKER_SEND_TASK_EVENTS = True
CELERY_TASK_SEND_SENT_EVENT = True

# django-rest-framework
# -------------------------------------------------------------------------------
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.TokenAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "EXCEPTION_HANDLER": "tools.django.exception_handler.custom_handler.custom_exception_handler",
    "DEFAULT_RENDERER_CLASSES": ("tools.django.exception_handler.renderer.ProjectRender",),
    "DEFAULT_FILTER_BACKENDS": (
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
    ),
}

# EXCEPTION HANDLER
# -------------------------------------------------------------------------------
EXCEPTIONS_HOG = {
    "EXCEPTION_REPORTING": "tools.django.exception_handler.handler.exception_reporter",
    "ENABLE_IN_DEBUG": False,
    "NESTED_KEY_SEPARATOR": "__",
    "SUPPORT_MULTIPLE_EXCEPTIONS": True,
}

# JWT
# -------------------------------------------------------------------------------
SIMPLE_JWT = {
    "AUTH_HEADER_TYPES": "jwt",
    "ACCESS_TOKEN_LIFETIME": datetime.timedelta(days=7),
    "REFRESH_TOKEN_LIFETIME": datetime.timedelta(days=14),
    "ROTATE_REFRESH_TOKENS": True,
}

# SWAGGER
# -------------------------------------------------------------------------------
SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'api_key': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization'
        }
    },
    'DOC_EXPANSION': 'none',
}

DATA_UPLOAD_MAX_NUMBER_FIELDS = 10000
