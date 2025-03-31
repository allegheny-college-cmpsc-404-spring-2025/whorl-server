import os
from dotenv import load_dotenv
import logging
import threading
import requests

# for writing logs to a file
import gzip
import shutil
import datetime
import schedule
import pathlib
import time
from logging.handlers import TimedRotatingFileHandler

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
    # "django_prometheus",
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
    "django_prometheus.middleware.PrometheusBeforeMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "core.middleware.GitHubTokenAuthenticationMiddleware",
    "django_prometheus.middleware.PrometheusAfterMiddleware",
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


class ScraperFilter(logging.Filter):
    def filter(self, record):
        arg = getattr(record, "args", None)
        if arg:
            if "/metrics" in arg[0]:
                return False
        return True


class RequestFilter(logging.Filter):
    """Filter by if it has a standard HTTP request format"""

    """
    A logging filter that allows log records with specific HTTP status codes to pass through.

    This filter checks if the log record contains arguments (`args`) and evaluates the second-to-last argument as an HTTP status code. Only status codes in the range 100-599 are allowed.
    """

    def filter(self, record):
        """
        Filters log records based on the presence of specific HTTP request types and status codes.

        This method evaluates whether a log record contains arguments (`args`) that include a valid HTTP status code
        and a recognized HTTP request type (e.g., POST, GET). If both conditions are met, the log record is allowed
        to pass through the filter.

        Args:
            record (logging.LogRecord): The log record to evaluate.

        Returns:
            bool: True if the log record contains a valid HTTP request type and status code, False otherwise.
        """
        request_types: set = {"POST", "GET", "PATCH", "DELETE"}
        http_status_codes: set = {
            "100",
            "101",
            "102",
            "103",
            "200",
            "201",
            "202",
            "203",
            "204",
            "205",
            "206",
            "207",
            "208",
            "226",
            "300",
            "301",
            "302",
            "303",
            "304",
            "305",
            "306",
            "307",
            "308",
            "400",
            "401",
            "402",
            "403",
            "404",
            "405",
            "406",
            "407",
            "408",
            "409",
            "410",
            "411",
            "412",
            "413",
            "414",
            "415",
            "416",
            "417",
            "418",
            "421",
            "422",
            "423",
            "424",
            "425",
            "426",
            "427",
            "428",
            "429",
            "431",
            "451",
            "500",
            "501",
            "502",
            "503",
            "504",
            "505",
            "506",
            "507",
            "508",
            "510",
            "511",
        }
        if getattr(record, "args", None):
            log_info = record.args
            if len(http_status_codes.intersection(set(log_info))):
                request = str(log_info[0])
                request = request.split(" ")
                if len(request_types.intersection(set(request))):
                    return True
            return False
        return False


LOGGING = {
    # Specifies the version of the logging configuration schema and whether to disable existing loggers.
    "version": 1,
    "disable_existing_loggers": False,
    # Formatters define the structure of log messages.
    "formatters": {
        "verbose": {
            "format": "[%(asctime)s] : %(levelname)s : %(message)s",
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
        "scraping_filter": {
            "()": "core.settings.ScraperFilter",
        },
    },
    # Handlers define where log messages are sent (e.g., files, console).
    "handlers": {
        "file_warning": {
            "level": "WARNING",
            "class": "logging.FileHandler",
            "filename": os.path.join(BASE_DIR, "logs/error.log"),
            "formatter": "verbose",
            "filters": ["warning_filter", "request_filter", "scraping_filter"],
        },
        "file_info": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": os.path.join(BASE_DIR, "logs/requests.log"),
            "formatter": "verbose",
            "filters": ["request_filter", "scraping_filter"],
        },
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
            "filters": ["request_filter", "scraping_filter"],
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
                "console",
            ],
            "level": "DEBUG",
            "propagate": False,
        },
    },
}

MODULE_PATH = pathlib.Path(__file__).parent.resolve()
path_to_file = os.path.join(MODULE_PATH, "python_scheduler.py")

# print(path_to_file)
# call the file that performs log saving
os.system(f"python {path_to_file}")
