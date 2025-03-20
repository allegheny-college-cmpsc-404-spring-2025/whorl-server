import os
from dotenv import load_dotenv
import logging

from pathlib import Path

# Versioning
REST_FRAMEWORK = {
    "DEFAULT_VERSIONING_CLASS": "rest_framework.versioning.NamespaceVersioning"
}

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-t6n*wl=xvln@*wvjh7_bv2&xi4wsyx8hl6qviiq$8)kn3zy^zr"

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv()

ALLOWED_HOSTS = ["localhost", "127.0.0.1", os.getenv("API_URL")]

CSRF_TRUSTED_ORIGINS = ["http://localhost", "http://127.0.0.1"]

DEBUG = True

# Load .env file
load_dotenv(dotenv_path=os.path.join(BASE_DIR, "srv/endpoints/.env"))

BASE_DIR = Path(__file__).resolve().parent.parent

# Database configuration
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "api",
        "USER": os.getenv("API_DB_USER"),
        "PASSWORD": os.getenv("API_DB_PASS"),
        "HOST": "localhost",
        "PORT": "",
    }
}

ROOT_URLCONF = "core.urls"

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "pgtrigger",
    "rest_framework",
    "drf_yasg",
    "core",
    "climate",
    "inventory",
    "omnipresence",
    "persona",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "core.middleware.GitHubTokenAuthenticationMiddleware",
]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Logging Configuration
# this will ignore django autoreloads and django db backend logs
# Custom Filter Class
class LevelFilter(logging.Filter):
    def __init__(self, level):
        self.level = level

    def filter(self, record):
        return record.levelname == self.level

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "[%(asctime)s] %(levelname)s: %(message)s",
        },
        "simple": {
            "format": "%(levelname)s: %(message)s",
        },
    },
    "filters": {
        "warning_filter": {
            "()": "core.settings.LevelFilter",
            "level": "WARNING",
        },
        "info_filter": {
            "()": "core.settings.LevelFilter",
            "level": "INFO",
        },
    },
    "handlers": {
        "file_warning": {
            "level": "WARNING",
            "class": "logging.FileHandler",
            "filename": os.path.join(BASE_DIR, "logs/error.log"),
            "formatter": "verbose",
            "filters": ["warning_filter"],
        },
        "file_info": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": os.path.join(BASE_DIR, "logs/successful.log"),
            "formatter": "verbose",
            "filters": ["info_filter"],
        },
        "file_debug": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": os.path.join(BASE_DIR, "logs/debug.log"),
            "formatter": "verbose",
        },
        "console_warning": {
            "level": "WARNING",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
            "filters": ["warning_filter"],
        },
        "console_info": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
            "filters": ["info_filter"],
        },
    },
    "loggers": {
        "django": {
            "handlers": ["file_warning", "file_info", "file_debug", "console_warning", "console_info"],
            "level": "DEBUG",
            "propagate": False,
        },
    },
}
