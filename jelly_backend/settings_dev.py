import os
from dotenv import load_dotenv
import dj_database_url
from jelly_backend.settings import *

load_dotenv()

DEBUG = True

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    'tecitostore.com',
    'api.tecitostore.com',
    '179.43.127.60',
]

DATABASES = {
    'default': dj_database_url.config(default=os.getenv('DATABASE_URL_DEV'))
}

CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
    'https://localhost:8081',
    'http://localhost:8000',
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

CSRF_COOKIE_SECURE = False
CSRF_COOKIE_HTTPONLY = False
CSRF_COOKIE_NAME = 'csrftoken'
CSRF_COOKIE_AGE = 31449600  # 1 año en segundos
CSRF_COOKIE_PATH = '/'
CSRF_HEADER_NAME = 'HTTP_X_CSRFTOKEN'
CSRF_TRUSTED_ORIGINS = [
    'http://localhost:3000',
    'https://localhost:8081',
    'http://localhost:8000',
    'https://tecitostore.com',
    'https://api.tecitostore.com',
]

CELERY_BROKER_URL = 'amqp://rabbitmq:5672'
CELERY_RESULT_BACKEND = 'rpc://'
