import os
from dotenv import load_dotenv
import dj_database_url
from jelly_backend.settings import *

load_dotenv()

DEBUG = False

ALLOWED_HOSTS = [
    'tecitostore.com',
    'api.tecitostore.com',
    '179.43.127.60',
]

DATABASES = {
    'default': dj_database_url.config(default=os.getenv('DATABASE_URL'))
}

CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS = [
    'https://tecitostore.com',
    'https://api.tecitostore.com',
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
CSRF_COOKIE_DOMAIN = '.tecitostore.com'
CSRF_TRUSTED_ORIGINS = [
    'https://tecitostore.com',
    'https://api.tecitostore.com',
]

CELERY_BROKER_URL = 'amqp://rabbitmq:5672'
