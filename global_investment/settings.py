
from pathlib import Path
import os

from dotenv import load_dotenv
from django.utils.translation import gettext_lazy as _


# ============================================================
# 1. PROJECT PATHS AND ENVIRONMENT
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from the local .env file
load_dotenv(BASE_DIR / ".env")


# ============================================================
# 2. SECURITY SETTINGS
# ============================================================

SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]

DEBUG = os.getenv("DJANGO_DEBUG", "True").lower() == "true"

ALLOWED_HOSTS = [
    host.strip()
    for host in os.getenv(
        "DJANGO_ALLOWED_HOSTS",
        "localhost,127.0.0.1"
    ).split(",")
    if host.strip()
]


# ============================================================
# 3. APPLICATIONS
# ============================================================

INSTALLED_APPS = [
    # Django applications
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sitemaps",

    # Third-party applications
    "rest_framework",
    "django_extensions",
    "captcha",

    # Project applications
    "users",
    "projects",

    # WhiteNoise development support
    "whitenoise.runserver_nostatic",
]


# ============================================================
# 4. MIDDLEWARE
# ============================================================

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",

    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


# ============================================================
# 5. URL CONFIGURATION
# ============================================================

ROOT_URLCONF = "global_investment.urls"

WSGI_APPLICATION = "global_investment.wsgi.application"


# ============================================================
# 6. TEMPLATES
# ============================================================

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",

        "DIRS": [
            BASE_DIR / "templates",
        ],

        "APP_DIRS": True,

        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",

                # Custom project context processors
                "projects.context_processors.unread_notifications",
                "projects.context_processors.languages_processor",
            ],
        },
    },
]


# ============================================================
# 7. DATABASE
# ============================================================

# SQLite for local development.
# We will configure PostgreSQL separately when preparing deployment.

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# ============================================================
# 8. CUSTOM USER MODEL
# ============================================================

AUTH_USER_MODEL = "users.CustomUser"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# ============================================================
# 9. PASSWORD VALIDATION
# ============================================================

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


# ============================================================
# 10. INTERNATIONALIZATION
# ============================================================

LANGUAGE_CODE = "en-us"

LANGUAGES = [
    ("en", _("English")),
    ("ar", _("Arabic")),
    ("ti", _("Eritrean Tigrinya")),
    ("sv", _("Svenska")),
    ("de", _("German")),
    ("ru", _("Russian")),
    ("zh-hans", _("Chinese")),
    ("it", _("Italian")),
    ("fr", _("French")),
]

TIME_ZONE = "UTC"

USE_I18N = True
USE_TZ = True

LOCALE_PATHS = [
    BASE_DIR / "locale",
]


# ============================================================
# 11. LOGIN AND LOGOUT
# ============================================================

LOGIN_URL = "login"

LOGIN_REDIRECT_URL = "/"

LOGOUT_REDIRECT_URL = "/"


# ============================================================
# 12. STATIC FILES
# ============================================================

STATIC_URL = "/static/"

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

STATIC_ROOT = BASE_DIR / "staticfiles"


# ============================================================
# 13. MEDIA FILES
# ============================================================

MEDIA_URL = "/media/"

MEDIA_ROOT = BASE_DIR / "media"


# ============================================================
# 14. GOOGLE RECAPTCHA
# ============================================================

RECAPTCHA_PUBLIC_KEY = os.getenv("RECAPTCHA_PUBLIC_KEY", "")

RECAPTCHA_PRIVATE_KEY = os.getenv("RECAPTCHA_PRIVATE_KEY", "")

RECAPTCHA_DEFAULT_ACTION = "generic"

RECAPTCHA_SCORE_THRESHOLD = 0.5


# ============================================================
# 15. PAYPAL CONFIGURATION
# ============================================================

PAYPAL_CLIENT_ID = os.getenv("PAYPAL_CLIENT_ID", "")

PAYPAL_SECRET = os.getenv("PAYPAL_SECRET", "")

PAYPAL_MODE = os.getenv("PAYPAL_MODE", "sandbox")


# ============================================================
# 16. EMAIL CONFIGURATION
# ============================================================

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

EMAIL_HOST = os.getenv("EMAIL_HOST", "smtp.gmail.com")

EMAIL_PORT = int(os.getenv("EMAIL_PORT", "587"))

EMAIL_USE_TLS = (
    os.getenv("EMAIL_USE_TLS", "True").lower() == "true"
)

EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER", "")

EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD", "")

DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

CONTACT_EMAIL = os.getenv("CONTACT_EMAIL", "")

ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "")


# ============================================================
# 17. HTTPS AND BROWSER SECURITY
# ============================================================

SECURE_SSL_REDIRECT = (
    os.getenv("DJANGO_SECURE_SSL_REDIRECT", "False").lower() == "true"
)

SESSION_COOKIE_SECURE = not DEBUG

CSRF_COOKIE_SECURE = not DEBUG

SECURE_CONTENT_TYPE_NOSNIFF = True

X_FRAME_OPTIONS = "DENY"

SECURE_REFERRER_POLICY = "same-origin"

# Enable HSTS only when production HTTPS is fully configured.

SECURE_HSTS_SECONDS = (
    int(os.getenv("DJANGO_SECURE_HSTS_SECONDS", "0"))
    if not DEBUG else 0
)

SECURE_HSTS_INCLUDE_SUBDOMAINS = False

SECURE_HSTS_PRELOAD = False


# ============================================================
# 18. LOGGING
# ============================================================

LOGGING = {
    "version": 1,

    "disable_existing_loggers": False,

    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },

    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
    },
}
