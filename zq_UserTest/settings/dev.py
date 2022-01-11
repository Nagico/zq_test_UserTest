import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

from .base import *

# debug 模式
DEBUG = True

ALLOWED_HOSTS = [
    '*'
]

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR.parent / 'db.sqlite3',
    }
}

# Sentry

sentry_sdk.init(
    dsn="https://178a4ca27b714010b507696efef1ce19@o1113532.ingest.sentry.io/6144088",
    integrations=[DjangoIntegration()],

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0,

    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True,

    environment="dev"
)
