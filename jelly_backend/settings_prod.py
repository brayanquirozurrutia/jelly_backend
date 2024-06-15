import os
from dotenv import load_dotenv
from jelly_backend.settings import *

load_dotenv()

DEBUG = False

ALLOWED_HOSTS = [
    'mi-dominio.com',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('NAME_PROD'),
        'USER': os.getenv('USER_PROD'),
        'PASSWORD': os.getenv('PASSWORD_PROD'),
        'HOST': os.getenv('HOST_PROD', 'localhost'),
        'PORT': os.getenv('PORT_PROD', '5432'),
    }
}

CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS = [
    'https://mi-dominio.com',
]
CORS_ALLOW_HEADERS = [
    'content-type',
    'authorization',
    'x-csrftoken',
]
CORS_ALLOW_METHODS = [
    'GET',
    'POST',
    'PUT',
    'PATCH',
    'DELETE',
    'OPTIONS',
]
CORS_EXPOSE_HEADERS = [
    'Content-Type',
    'X-CSRFToken',
]

CSRF_COOKIE_AGE = 31449600  # 1 año en segundos
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_NAME = 'csrftoken'
CSRF_HEADER_NAME = 'HTTP_X_CSRFTOKEN'
CSRF_COOKIE_PATH = '/'
CSRF_COOKIE_DOMAIN = '.mi-dominio.com'
CSRF_TRUSTED_ORIGINS = [
    'https://mi-dominio.com',
]
