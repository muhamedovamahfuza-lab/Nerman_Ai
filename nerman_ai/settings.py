from pathlib import Path
from decouple import config
import dj_database_url
import os

BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = config('SECRET_KEY', default='django-insecure-default-key-change-this')
DEBUG = config('DEBUG', default=True, cast=bool)
ALLOWED_HOSTS = ['*']

CSRF_TRUSTED_ORIGINS = [
    'https://nerman-ai-test.onrender.com',
    'https://nerman-ai.onrender.com',
    'https://nerman-ai-kcij.onrender.com'
]


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Third party apps
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.github',
    'rest_framework',
    'core',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'nerman_ai.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'nerman_ai.wsgi.application'


DATABASE_URL = config('DATABASE_URL', default=None)

if DATABASE_URL:
    DATABASES = {
        'default': dj_database_url.config(default=DATABASE_URL, conn_max_age=600)
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }


AUTH_USER_MODEL = 'core.User'

from django.utils.translation import gettext_lazy as _

# Internationalization
LANGUAGE_CODE = 'ru'
TIME_ZONE = 'Asia/Tashkent'
USE_I18N = True
USE_TZ = True

LANGUAGES = [
    ('ru', _('Русский')),
    ('en', _('English')),
    ('uz', _('O\'zbek')),
]

LOCALE_PATHS = [
    BASE_DIR / 'locale',
]


STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


LOGIN_URL = '/auth/login/'
LOGIN_REDIRECT_URL = '/dashboard/'
LOGOUT_REDIRECT_URL = '/'


AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

SITE_ID = 1
ACCOUNT_LOGIN_METHODS = {'email'}
ACCOUNT_SIGNUP_FIELDS = ['email*', 'password1*', 'password2*']
ACCOUNT_EMAIL_VERIFICATION = 'optional'

EMAIL_BACKEND = config('EMAIL_BACKEND', default='django.core.mail.backends.console.EmailBackend')

# ============================================
# AI Service Configuration
# ============================================
AI_API_KEY = config('AI_API_KEY', default=None)
AI_API_TYPE = config('AI_API_TYPE', default='gemini')  # 'openai' or 'gemini'

# Startup validation and logging for AI configuration
import logging
logger = logging.getLogger(__name__)

if AI_API_KEY:
    logger.info(f"✓ AI_API_KEY is configured (using {AI_API_TYPE})")
else:
    logger.warning("⚠ AI_API_KEY is not set! AI chat will not work. Set AI_API_KEY in environment variables.")
    logger.warning("   For Render.com: Add AI_API_KEY in Environment tab")
    logger.warning("   For local dev: Add AI_API_KEY to .env file")

if AI_API_TYPE not in ['openai', 'gemini']:
    logger.warning(f"⚠ Invalid AI_API_TYPE: {AI_API_TYPE}. Must be 'openai' or 'gemini'. Defaulting to 'gemini'.")
    AI_API_TYPE = 'gemini'
