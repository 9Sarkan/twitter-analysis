import os
from commons.utils import get_env

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_DIR = os.path.dirname(BASE_DIR)

PROJECT_NAME = get_env("PROJECT_NAME", raise_exception=True)

PROJECT_DESCRIPTION = get_env("PROJECT_DESCRIPTION", raise_exception=True)

PROJECT_DOMAIN_NAME = get_env("PROJECT_DOMAIN_NAME", raise_exception=True)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = get_env("SECRET_KEY", raise_exception=True)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = int(get_env("DEBUG", raise_exception=True))

ALLOWED_HOSTS = get_env("ALLOWED_HOSTS", raise_exception=True).split(",")

# Application definition

INSTALLED_APPS = [
    # Defaults
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Third Parties
    "corsheaders",
    # Locals
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "base.urls"
CORS_ORIGIN_ALLOW_ALL = True
# Media files

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(PROJECT_DIR, "media")

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

WSGI_APPLICATION = "base.wsgi.application"

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": get_env("DB_NAME", raise_exception=True),
        "USER": get_env("DB_USER", raise_exception=True),
        "PASSWORD": get_env("DB_PASSWORD", raise_exception=True),
        "HOST": get_env("DB_HOST", raise_exception=True),
        "PORT": get_env("DB_PORT", raise_exception=True),
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation"
        ".UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation" ".MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation" ".CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation" ".NumericPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = False
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]


# Datetime format settings
DATETIME_FORMAT = "l, M d Y h:i:s A"
DATE_FORMAT = "l, M d Y"
TIME_FORMAT = "h:i:s A"

admins_email = get_env("ADMINS_EMAIL", "").split(",")
ADMINS = [admin.split(":") for admin in admins_email]
ADMIN_USER = get_env("ADMIN_USER", raise_exception=True)

# Site settings
SITE = {
    "NAME": get_env("SITE_NAME", ""),
    "DESCRIPTION": get_env("PROJECT_DESCRIPTION", ""),
    "DOMAIN": get_env("SITE_DOMAIN", "http://localhost:8000"),
}

# Django Logger
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "WARNING",
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": get_env("DJANGO_LOG_LEVEL", raise_exception=True),
            "propagate": False,
        },
    },
}

