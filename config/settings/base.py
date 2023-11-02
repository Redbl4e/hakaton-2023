from os import getenv
from pathlib import Path

from dotenv import load_dotenv
from firebase_admin import initialize_app
from rest_framework.reverse import reverse

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv()

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-_)noqum!!s^eg1*34ysh1+hm#tw^#rafz&p&fvl6n_-#c$n^j9'

AUTH_USER_MODEL = 'users.User'
AUTHENTICATION_BACKENDS = ['users.backend.EmailBackend']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'drf_yasg',
    'rest_framework.apps.RestFrameworkConfig',
    'fcm_django',
    'channels',
    'coordinat.apps.CoordinatConfig',
    'users.apps.UsersConfig',
    'incidents.apps.IncidentsConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

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

WSGI_APPLICATION = 'config.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'USER': getenv('POSTGRES_USERNAME'),
        'PASSWORD': getenv('POSTGRES_PASSWORD'),
        'HOST': getenv('POSTGRES_HOST'),
        'PORT': getenv('POSTGRES_PORT'),
        'NAME': getenv('POSTGRES_DBNAME')
    }
}

# Internationalization
LANGUAGE_CODE = 'ru-RU'
TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_TZ = True

# Static
STATIC_URL = 'staticfiles/'
STATIC_ROOT = BASE_DIR / 'staticfiles/'
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media/'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Swagger
SWAGGER_SETTINGS = {
    'LOGIN_URL': '/api/user/login/',
    'LOGOUT_URL': '/api/user/logout/'
}

FIREBASE_APP = initialize_app()

FCM_DJANGO_SETTINGS = {
    "APP_VERBOSE_NAME": "My FCM Project",
    "FCM_SERVER_KEY": "your_fcm_server_key_here",
}

ASGI_APPLICATION = "config.asgi.application"
