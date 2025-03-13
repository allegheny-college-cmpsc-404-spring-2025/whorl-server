import os
from dotenv import load_dotenv

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

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {message}",
            "datefmt": "%d/%b/%Y %H:%M:%S",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
        "error_file": {
            "level": "WARNING",
            "class": "logging.handlers.TimedRotatingFileHandler",
            "when": "D",
            "filename": os.path.join(BASE_DIR, "logs/error.log"),
            "formatter": "verbose",
        },
        "debug_file": {
            "level": "DEBUG",
            "class": "logging.handlers.TimedRotatingFileHandler",
            "when": "D",
            "filename": os.path.join(BASE_DIR, "logs/debug.log"),
            "formatter": "simple",
        },
        "successful_file": {
            "level": "INFO",
            "class": "logging.handlers.TimedRotatingFileHandler",
            "when": "D",
            "filename": os.path.join(BASE_DIR, "logs/successful.log"),
            "formatter": "simple",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["debug_file"],
            "level": "DEBUG",
            "propagate": True,
        },
        "django.request": {
            "handlers": ["console", "error_file"],
            "level": "WARNING",
            "propagate": False,
        },
        "django.db.backends": {
            "handlers": ["console", "successful_file"],
            "level": "INFO",
            "propagate": False,
        },
    },
}
