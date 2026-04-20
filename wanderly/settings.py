import os
from pathlib import Path
from decouple import config, Csv

BASE_DIR = Path(__file__).resolve().parent.parent

# ─────────────────────────────────────────────
# Core
# ─────────────────────────────────────────────
SECRET_KEY = config('SECRET_KEY', default='django-insecure-change-me-in-production')
DEBUG = config('DEBUG', default=True, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='*', cast=Csv())

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'cloudinary_storage',
    'django.contrib.staticfiles',
    'cloudinary',
    'channels',
    'accounts',
    'partners',
    'locations',
    'posts',
    'booking',
    'flights',
    'chat',
    'notifications',
    'reviews',
    'core',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',   # serve static files
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'wanderly.urls'

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

WSGI_APPLICATION = 'wanderly.wsgi.application'
ASGI_APPLICATION  = 'wanderly.asgi.application'

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer',
    },
}

# ─────────────────────────────────────────────
# Database
# Uses PostgreSQL on Render (DATABASE_URL env var),
# falls back to SQLite for local development.
# ─────────────────────────────────────────────
DATABASE_URL = config('DATABASE_URL', default='')

if DATABASE_URL:
    import dj_database_url
    DATABASES = {
        'default': dj_database_url.parse(DATABASE_URL, conn_max_age=600)
    }
else:
    # Local development — SQLite
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# ─────────────────────────────────────────────
# Auth
# ─────────────────────────────────────────────
AUTH_USER_MODEL        = 'accounts.User'
LOGIN_URL              = '/accounts/login/'
LOGIN_REDIRECT_URL     = '/'
LOGOUT_REDIRECT_URL    = '/'

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ─────────────────────────────────────────────
# Internationalisation
# ─────────────────────────────────────────────
LANGUAGE_CODE = 'en-us'
TIME_ZONE     = 'UTC'
USE_I18N      = True
USE_TZ        = True

# ─────────────────────────────────────────────
# Static files  (WhiteNoise serves them on Render)
# ─────────────────────────────────────────────
STATIC_URL  = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

# CompressedManifestStaticFilesStorage requires collectstatic to have been run.
# Use it only in production; fall back to CompressedStaticFilesStorage locally
# so CSS/JS load correctly with just `runserver` without needing collectstatic.
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'# ─────────────────────────────────────────────
# Media files  (Cloudinary stores them forever)
# ─────────────────────────────────────────────
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': config('CLOUDINARY_CLOUD_NAME', default=''),
    'API_KEY':    config('CLOUDINARY_API_KEY',    default=''),
    'API_SECRET': config('CLOUDINARY_API_SECRET', default=''),
}

# Use Cloudinary only when credentials are provided (i.e. in production)
if all([
    config('CLOUDINARY_CLOUD_NAME', default=''),
    config('CLOUDINARY_API_KEY',    default=''),
    config('CLOUDINARY_API_SECRET', default=''),
]):
    DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
    MEDIA_URL = f"https://res.cloudinary.com/{config('CLOUDINARY_CLOUD_NAME')}/"
else:
    # Local development — store media on disk
    MEDIA_URL  = '/media/'
    MEDIA_ROOT = BASE_DIR / 'media'

# ─────────────────────────────────────────────
# External APIs
# ─────────────────────────────────────────────
WEATHER_API_KEY = config('WEATHER_API_KEY', default='')
WEATHER_API_URL = 'https://api.openweathermap.org/data/2.5/weather'

AMADEUS_API_KEY    = config('AMADEUS_API_KEY',    default='')
AMADEUS_API_SECRET = config('AMADEUS_API_SECRET', default='')

# ─────────────────────────────────────────────
# App-level limits
# ─────────────────────────────────────────────
DEFAULT_AUTO_FIELD    = 'django.db.models.BigAutoField'
CHAT_MESSAGE_EXPIRY_DAYS = 180
POST_LIMIT_PER_PARTNER   = 5
MAX_PLACES_PER_CITY      = 20
MAX_IMAGES_PER_POST      = 5
