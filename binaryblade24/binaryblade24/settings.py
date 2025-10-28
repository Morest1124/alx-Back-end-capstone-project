"""
Django settings for binaryblade24 project.
"""

from pathlib import Path
import os
from dotenv import load_dotenv
import dj_database_url
from datetime import timedelta
import os
from django.core.exceptions import ImproperlyConfigured


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from .env file
load_dotenv()

# --- Core Production Settings ---

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

# 🗝️ Read the key from the environment variable set in the WSGI file.
SECRET_KEY = os.environ.get('SECRET_KEY')

if not SECRET_KEY:
    # This check ensures the app fails early if the key is somehow missing
    raise ImproperlyConfigured("The SECRET_KEY setting must not be empty. Check your PythonAnywhere WSGI file.")

# SECURITY WARNING: don't run with debug turned on in production!
# Debug will be 'True' only if the DEBUG environment variable is explicitly set to 'true'.
# DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'
DEBUG = False

# Define the allowed hosts for your application.
# In production, this should be your domain name(s), e.g., 'www.example.com'.
# It's loaded from an environment variable for flexibility.
ALLOWED_HOSTS = ["binaryblade2411.pythonanywhere.com"]


# --- Application Definition ---

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders', # For Cross-Origin Resource Sharing
    'User',
    'Project',
    'Proposal',
    'Review',
    'Comment',
    'dashboard',
    'message',
    'rest_framework_api_key', 
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # WhiteNoise middleware for serving static files efficiently in production
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware', # CORS middleware
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'binaryblade24.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'binaryblade24.wsgi.application'


# --- Database Configuration ---
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases
# Uses dj_database_url to parse the DATABASE_URL environment variable (e.g., for PostgreSQL).
# Falls back to a local SQLite database for development if DATABASE_URL is not set.
DATABASES = {
    'default': dj_database_url.config(
        default=f'sqlite:///{BASE_DIR / "db.sqlite3"}',
        conn_max_age=600
    )
}


# --- Password Validation ---
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# --- Internationalization & Timezones ---
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# --- Static & Media Files ---
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = 'static/'
# The directory where collectstatic will gather all static files for production.
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Using WhiteNoise for efficient static file storage and serving in production.
STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# --- Authentication & API Settings ---

# Use the custom user model defined in the User app
AUTH_USER_MODEL = 'User.User'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
}

# In production, this should be the URL of your frontend application.
CORS_ALLOWED_ORIGINS = os.environ.get('CORS_ALLOWED_ORIGINS', 'http://localhost:3000').split(',')


# --- Production Security Settings ---
# These settings are critical for running in a production environment with HTTPS.
if not DEBUG:
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_SSL_REDIRECT = True
    SECURE_HSTS_SECONDS = 31536000  # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

# --- Logging Configuration ---
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'debug.log'),
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': True,
        },
        'User': { # Logger for your User app
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False, # Don't pass to django logger
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'INFO',
    },
}