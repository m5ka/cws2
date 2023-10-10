"""
cws2 settings

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/

For a reference on using environ, see
https://github.com/joke2k/django-environ
"""

from pathlib import Path

import environ

# Define initial environment
env = environ.Env()


# Base directories for setting absolute paths
# This is the root repository directory.
# The app directory is BASE_DIR / "cws2"
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent.parent


# Read environment variables from .env
env.read_env(BASE_DIR / ".env")


# Debug
# Warning! This should only be True on local development copies
# https://docs.djangoproject.com/en/4.1/ref/settings/#std-setting-DEBUG
DEBUG = env.bool("DEBUG", default=False)


# Application definition
# https://docs.djangoproject.com/en/4.1/ref/applications/
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_jinja",
    "django_jinja.contrib._humanize",
    "django_sass",
    "captcha",
    "cws2",
]


# Middleware
# https://docs.djangoproject.com/en/4.1/topics/http/middleware/
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "cws2.middleware.LogUserLastSeenMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


# Debug toolbar
# https://django-debug-toolbar.readthedocs.io/en/latest/
if DEBUG and env.bool("DEBUG_TOOLBAR", default=True):
    try:
        import debug_toolbar  # noqa: F401

        INSTALLED_APPS += ["debug_toolbar"]
        MIDDLEWARE = ["debug_toolbar.middleware.DebugToolbarMiddleware"] + MIDDLEWARE
        DEBUG_TOOLBAR = True
    except ImportError:
        DEBUG_TOOLBAR = False
else:
    DEBUG_TOOLBAR = False


# Django extensions (development only)
# https://django-extensions.readthedocs.io/en/latest/
if DEBUG:
    try:
        import django_extensions  # noqa: F401

        INSTALLED_APPS += ["django_extensions"]
    except ImportError:
        pass


# Root URL configuration
# https://docs.djangoproject.com/en/4.1/ref/settings/#root-urlconf
ROOT_URLCONF = "cws2.config.urls"


# Template configuration
# https://docs.djangoproject.com/en/4.1/ref/settings/#templates
TEMPLATES = [
    {
        "BACKEND": "django_jinja.backend.Jinja2",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.debug",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
            ],
            "policies": {
                "ext.i18n.trimmed": True,
            },
        },
    },
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


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases
DATABASES = {
    "default": env.db(
        "DATABASE_URL",
        engine="postgres",
        default="postgres://localhost:5432/cws2",
    ),
}


# WSGI application definition
WSGI_APPLICATION = "cws2.config.wsgi.application"


# Authentication
# https://docs.djangoproject.com/en/3.2/topics/auth/customizing/#auth-custom-user
AUTH_USER_MODEL = "cws2.User"
LOGIN_URL = "login"


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
        ),
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
# https://docs.djangoproject.com/en/4.1/topics/i18n/
LANGUAGE_CODE = "en-gb"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True


# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# Secret key for cryptographic signing
# SECURITY WARNING: keep the secret key used in production secret!
# https://docs.djangoproject.com/en/4.1/ref/settings/#secret-key
SECRET_KEY = env.str(
    "SECRET_KEY",
    default="cws2-keyboard-cat",
)


# List of hostnames to accept requests from
# https://docs.djangoproject.com/en/4.1/ref/settings/#allowed-hosts
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", cast=str, default=[])


# CSRF trusted origins
# https://docs.djangoproject.com/en/4.1/ref/settings/#csrf-trusted-origins
CSRF_TRUSTED_ORIGINS = env.list("CSRF_TRUSTED_ORIGINS", cast=str, default=[])


# Internal IPs
# https://docs.djangoproject.com/en/4.1/ref/settings/#internal-ips
INTERNAL_IPS = [
    "127.0.0.1",
]


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/
STATIC_URL = env.str("STATIC_URL", default="static/")
STATIC_ROOT = BASE_DIR / "cws2/static"


# User-uploaded content
# https://docs.djangoproject.com/en/4.2/ref/settings/#std-setting-MEDIA_ROOT
MEDIA_URL = env.str("MEDIA_URL", default="media/")
MEDIA_ROOT = BASE_DIR / "media"


# Email settings
# https://docs.djangoproject.com/en/4.1/topics/email/
EMAIL_FROM = env.str("EMAIL_FROM", default='"Sender" <sender@example.com>')
EMAIL_HOST = env.str("EMAIL_HOST", default="localhost")
EMAIL_PORT = env.int("EMAIL_PORT", default=25)
EMAIL_HOST_USER = env.str("EMAIL_HOST_USER", default="")
EMAIL_HOST_PASSWORD = env.str("EMAIL_HOST_PASSWORD", default="")
EMAIL_USE_TLS = env.bool("EMAIL_USE_TLS", default=False)
EMAIL_USE_SSL = env.bool("EMAIL_USE_SSL", default=False)
EMAIL_TIMEOUT = env.int("EMAIL_TIMEOUT", default=3)


# Username settings
USERNAME_MIN_LENGTH = 3
USERNAME_MAX_LENGTH = 36


# URL configuration
SITE_ROOT_URL = env.str("SITE_ROOT_URL", default="https://conworkshop.com")


# Recaptcha settings
# https://pypi.org/project/django-recaptcha/#installation
if DEBUG:
    SILENCED_SYSTEM_CHECKS = ["captcha.recaptcha_test_key_error"]
else:
    RECAPTCHA_PUBLIC_KEY = env.str("RECAPTCHA_PUBLIC_KEY")
    RECAPTCHA_PRIVATE_KEY = env.str("RECAPTCHA_PRIVATE_KEY")
