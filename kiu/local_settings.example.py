# This file contains all the settings that defines the local server
# Create local_settings.py to override any settings here

import logging

from django.conf import settings


DEBUG = True

# Installed apps for development only:
INSTALLED_APPS = settings.INSTALLED_APPS + ["django_extensions", "nplusone.ext.django"]

MIDDLEWARE = [  # noqa: WPS440
    "nplusone.ext.django.NPlusOneMiddleware",
] + settings.MIDDLEWARE


ALLOWED_HOSTS = ["*"]

# Disable persistent DB connections
# https://docs.djangoproject.com/en/3.2/ref/databases/#caveats
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "kiu",
        "USER": "postgres",
        "PASSWORD": "postgres",
        "HOST": "localhost",
        "PORT": "5432",
    }
}

# nplusone
# https://github.com/jmcarp/nplusone
# Logging N+1 requests:
NPLUSONE_RAISE = False  # comment out if you want to allow N+1 requests
NPLUSONE_LOGGER = logging.getLogger("django")
NPLUSONE_LOG_LEVEL = logging.WARN

# Logging
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,  # if set True will show django requests with status codes, etc
    "handlers": {
        "file": {  # Write logs to file
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": "/tmp/debug.log",
            "formatter": "verbose",
        },
        "console": {"class": "logging.StreamHandler", "formatter": "verbose"},
    },
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(module)s "
            "%(process)d %(thread)d %(message)s"
        },
    },
    "loggers": {
        "": {  # App logging
            "level": "INFO",  # Can set ERROR if you can see a lot of logs in console
            "handlers": ["console", "file"],
            "propagate": True,
        },
        "django.db.backends": {  # Show SQL queries
            "level": "DEBUG",  # Disable database logging by setting to ERROR
            "handlers": ["console", "file"],
            "propagate": False,
        },
    },
}
