"""
Django settings for binaryblade24 project.
"""

from pathlib import Path
import os
from dotenv import load_dotenv
import dj_database_url # <--- NEW IMPORT

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production

# SECURITY WARNING: keep the secret key used in production secret!
load_dotenv()
SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
# Checks environment variable (Render sets this to 'False' or leaves it unset)
DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'

# CRITICAL: Dynamically set ALLOWED_HOSTS for production
# Render will set the HOST to your-app.onrender.com. 
# We split the environment variable by comma for multiple hosts.
if not DEBUG:
    # Use environment variable in production, fall back to '*' if necessary (less secure)
    ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')
else:
    # Local development hosts
    ALLOWED_HOSTS = ['localhost', '127.0.0.1']


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt',
    'User',
    'Project',
    'Proposal',
    'Review',
    'Comment',
    'dashboard',
    'message',
    # Note: 'whitenoise.runserver_nostatic' can be added here if you want to use WhiteNoise 
    # to serve static files locally while running 'manage.py runserver --nostatic'.
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}

from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # WhiteNoise must be placed immediately after SecurityMiddleware
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
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
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'binaryblade24.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases
# Use dj_database_url to parse the DATABASE_URL environment variable.
# Fallback to a local SQLite database for development if DATABASE_URL is not set.
DATABASES = {
    'default': dj_database_url.config(
        default=f'sqlite:///{BASE_DIR / "db.sqlite3"}',
        conn_max_age=600
    )
}


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
# DEPRECATED: STATIC_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
# CORRECTED: Use the modern STORAGES setting for WhiteNoise (essential for production)
STORAGES = {
    # Default file storage remains 'default'
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}


# Media files (User uploaded content)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# NOTE: For production, MEDIA_ROOT should be configured to use a persistent file 
# storage service like Amazon S3 or Render Disks, as local files are ephemeral.


# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Use the custom user model defined in the User app
AUTH_USER_MODEL = 'User.User'

CORS_ALLOWED_ORIGINS = [
    "http://localhost:8000",
    # Add your Render frontend URL here, e.g., "https://your-frontend.onrender.com"
]

# CRITICAL SECURITY SETTINGS FOR PRODUCTION (HTTPS)
# Render forces HTTPS, so these MUST be set to True.
if not DEBUG:
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_SSL_REDIRECT = True # Redirect HTTP to HTTPS
    SECURE_HSTS_SECONDS = 31536000 # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

# Stripe settings
# STRIPE_SECRET_KEY = os.environ.get('STRIPE_SECRET_KEY')
# STRIPE_WEBHOOK_SECRET = os.environ.get('STRIPE_WEBHOOK_SECRET')
# SITE_URL = os.environ.get('SITE_URL')

# PayPal settings
# PAYPAL_MODE = os.environ.get('PAYPAL_MODE', 'sandbox') # Or 'live' for production
# PAYPAL_CLIENT_ID = os.environ.get('PAYPAL_CLIENT_ID')
# PAYPAL_CLIENT_SECRET = os.environ.get('PAYPAL_CLIENT_SECRET')

# Custom User Model
AUTH_USER_MODEL = 'User.User'
