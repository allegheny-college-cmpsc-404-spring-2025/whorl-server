import os
from dotenv import load_dotenv
import logging
import threading
import requests

from pathlib import Path

# If a logs directory exists, use it; otherwise, create it
BASE_DIR = Path(__file__).resolve().parent.parent
# Define the path for the logs directory within the base directory.
LOGS_DIR = os.path.join(BASE_DIR, "logs")
# Check if the logs directory exists. If it does not, create it.
if not os.path.exists(LOGS_DIR):
    os.makedirs(LOGS_DIR)

# Versioning
REST_FRAMEWORK = {
    "DEFAULT_VERSIONING_CLASS": "rest_framework.versioning.NamespaceVersioning"
}

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-t6n*wl=xvln@*wvjh7_bv2&xi4wsyx8hl6qviiq$8)kn3zy^zr"

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# If a logs directory exists, use it; otherwise, create it

LOGS_DIR = os.path.join(BASE_DIR, "logs")
if not os.path.exists(LOGS_DIR):
    os.makedirs(LOGS_DIR)


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

class LevelFilter(logging.Filter):
    """
    A logging filter that allows log records with a specific log level to pass through.

    Attributes:
        level (str): The log level (e.g., "INFO", "WARNING") to filter for.
    """

    def __init__(self, level):
        """
        Initialize the LevelFilter with the specified log level.

        Args:
            level (str): The log level to filter for.
        """
        self.level = level

    def filter(self, record):
        """
        Determine if the log record matches the specified log level.

        Args:
            record (logging.LogRecord): The log record to evaluate.

        Returns:
            bool: True if the log record's level matches the specified level, False otherwise.
        """
        return record.levelname == self.level


class RequestFilter(logging.Filter):
    """
    A logging filter that allows log records with specific HTTP status codes to pass through.

    This filter checks if the log record contains arguments (`args`) and evaluates the second-to-last argument as an HTTP status code. Only status codes in the range 100-599 are allowed.
    """

    def filter(self, record):
        """
        Determine if the log record contains a valid HTTP status code in the range 100-599.

        Args:
            record (logging.LogRecord): The log record to evaluate.

        Returns:
            bool: True if the log record contains a valid HTTP status code, False otherwise.
        """
        if getattr(record, "args", None):
            log_info = record.args
            try:
                code = log_info[-2]
                code = int(code)
                if code >= 100 and code < 600:
                    return True
                return False
            except:
                return False
        return False


LOGGING = {
    # Specifies the version of the logging configuration schema and whether to disable existing loggers.
    "version": 1,
    "disable_existing_loggers": False,

    # Formatters define the structure of log messages.
    "formatters": {
        "verbose": {
            "format": "[%(asctime)s]: %(levelname)s : %(message)s",
        },
        "simple": {
            "format": "%(levelname)s : %(message)s",
        },
    },

    # Filters control which log records are processed based on custom criteria.
    "filters": {
        "warning_filter": {
            "()": "core.settings.LevelFilter",
            "level": "WARNING",
        },
        "info_filter": {
            "()": "core.settings.LevelFilter",
            "level": "INFO",
        },
        "request_filter": {
            "()": "core.settings.RequestFilter",
        },
    },

    # Handlers define where log messages are sent (e.g., files, console).
    "handlers": {
        "file_warning": {
            "level": "WARNING",
            "class": "logging.FileHandler",
            "filename": os.path.join(BASE_DIR, "logs/error.log"),
            "formatter": "verbose",
            "filters": ["warning_filter", "request_filter"],
        },
        "file_info": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": os.path.join(BASE_DIR, "logs/successful.log"),
            "formatter": "verbose",
            "filters": ["info_filter", "request_filter"],
        },
        "console_warning": {
            "level": "WARNING",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
            "filters": ["warning_filter", "request_filter"],
        },
        "console_info": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
            "filters": ["info_filter", "request_filter"],
        },
        "file_debug": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": os.path.join(BASE_DIR, "logs/debug.log"),
            "formatter": "verbose",
        },
    },

    # Loggers define the configuration for specific logging categories.
    "loggers": {
        "django": {
            "handlers": [
                "file_warning",
                "file_info",
                "file_debug",
                "console_warning",
                "console_info",
            ],
            "level": "DEBUG",
            "propagate": False,
        },
    },
}
