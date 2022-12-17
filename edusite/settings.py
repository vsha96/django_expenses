"""
Django settings for edusite project.

Generated by 'django-admin startproject' using Django 4.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path

import os
from dotenv import load_dotenv
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# hidden in the .env file
SECRET_KEY = str(os.getenv('SECRET_KEY'))


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    "expenses.apps.ExpensesConfig",
    # replaced with custom admin
    # "django.contrib.admin",
    'expenses.apps.CustomAdminConfig',
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "social_django",
    # for Jupyter-notebook
    "django_extensions",

    # for slick reports
    # DELETED
    # "slick_reporting",
    # "crispy_forms",
]

# for slick reports
# DELETED
# CRISPY_TEMPLATE_PACK = 'bootstrap4'

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    'social_django.middleware.SocialAuthExceptionMiddleware',
]

ROOT_URLCONF = "edusite.urls"

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
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = "edusite.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {

        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'app_django_expenses',
        'USER': 'vsha96',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '5432',
    }

    # You may change database to sqlite3
    # "default": {
    #     "ENGINE": "django.db.backends.sqlite3",
    #     "NAME": BASE_DIR / "db.sqlite3",
    # } 
}

# ===================
# ===== LOGGING =====
# ===================

# sentry
# import sentry_sdk
# from sentry_sdk.integrations.django import DjangoIntegration

# sentry_sdk.init(
#     dsn= str(os.getenv('SENTRY_DSN_KEY')),
#     integrations=[DjangoIntegration()],

#     # Set traces_sample_rate to 1.0 to capture 100%
#     # of transactions for performance monitoring.
#     # We recommend adjusting this value in production,
#     traces_sample_rate=1.0,

#     # If you wish to associate users to errors (assuming you are using
#     # django.contrib.auth) you may enable sending PII data.
#     send_default_pii=True,

#     # By default the SDK will try to use the SENTRY_RELEASE
#     # environment variable, or infer a git commit
#     # SHA as release, however you may want to set
#     # something more human-readable.
#     # release="myapp@1.0.0",
# )

# django logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,

    'formatters': {
        'verbose': {
            'format': '{asctime} {name} :: {levelname} :: {message}',
            'style': '{',
        },
    },

    'handlers': {
        'file-sql': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'logs/sql.log',
            'formatter': 'verbose',
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'logs/general.log',
            'formatter': 'verbose',
        },
    },

    'loggers': {
        'django.db.backends': {
            'handlers': ['file-sql'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'expenses.views' : {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        }
    },
}


# ===================
# === SOCIAL AUTH ===
# ===================

AUTHENTICATION_BACKENDS = [
    # 'social_core.backends.twitter.TwitterOAuth',
    'social_core.backends.twitch.TwitchOAuth2',
    'django.contrib.auth.backends.ModelBackend',
]

SOCIAL_AUTH_JSONFIELD_ENABLED = True

# SOCIAL_AUTH_URL_NAMESPACE = 'social'
LOGIN_URL = 'http://localhost/expenses/'
LOGOUT_URL = 'http://localhost/expenses/'
# LOGIN_REDIRECT_URL = 'http://localhost'
SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/complete/twitch/'


# hidden in the .env file
SOCIAL_AUTH_TWITCH_KEY = str(os.getenv('SOCIAL_AUTH_TWITCH_KEY'))
SOCIAL_AUTH_TWITCH_SECRET = str(os.getenv('SOCIAL_AUTH_TWITCH_SECRET'))

SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username',
    'social_core.pipeline.user.create_user',
    'expenses.views_oauth.create_account_oauth',  # <--- custom function
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details'
)


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",},
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# REST API settings
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    # 'DEFAULT_PERMISSION_CLASSES': [
    #     'rest_framework.permissions.AllowAny',
    # ]
}

