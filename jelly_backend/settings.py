import os
from pathlib import Path
from datetime import timedelta
from dotenv import load_dotenv
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv()

ENVIRONMENT = os.environ.get('DJANGO_ENV', 'development')

SECRET_KEY = os.getenv('SECRET_KEY')

INSTALLED_APPS = [
    # Django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'debug_toolbar',
    'drf_yasg',
    'rest_framework_simplejwt',
    'corsheaders',
    'graphene_django',
    'celery',
    'whitenoise.runserver_nostatic',
    # Custom apps
    'authentication',
    'users',
    'users_tokens',
    'products',
    'admin_app',
]

MIDDLEWARE = [
    'django.middleware.gzip.GZipMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_ratelimit.middleware.RatelimitMiddleware',
    # Custom middleware
    'jelly_backend.middleware.JWTAuthCookieMiddleware',
]

ROOT_URLCONF = 'jelly_backend.urls'

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

WSGI_APPLICATION = 'jelly_backend.wsgi.application'

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': ['rest_framework.permissions.IsAuthenticated'],
    'EXCEPTION_HANDLER': 'jelly_backend.exceptions.custom_exception_handler',
}

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header',
            'bearerFormat': 'JWT',
            'scheme': 'bearer',
            'description': "Enter your Bearer token in the format **'Bearer &lt;token&gt;'**",
        }
    },
    'SECURITY': [{'Bearer': []}],
    'USE_SESSION_AUTH': False,
}

AUTH_USER_MODEL = 'users.User'

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
}

GRAPHENE = {
    "SCHEMA": "jelly_backend.schema.schema"
}

CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL')
CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND', None)
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE

CELERY_WORKER_CONCURRENCY = 2
CELERY_WORKER_PREFETCH_MULTIPLIER = 1
CELERY_TASK_SOFT_TIME_LIMIT = 300
CELERY_TASK_ACKS_LATE = True
CELERY_WORKER_MAX_TASKS_PER_CHILD = 10

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}

DATABASES = {
    'default': dj_database_url.config(default=os.getenv('DATABASE_URL'))
}

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': os.getenv('REDIS_URL'),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

CORS_ALLOW_HEADERS = [
    'Content-Type',
    'Accept',
    'Authorization',
    'X-CSRFToken',
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
    'Authorization',
    'Accept',
]

CORS_ALLOW_CREDENTIALS = True

CSRF_COOKIE_NAME = 'csrftoken'
CSRF_HEADER_NAME = 'HTTP_X_CSRFTOKEN'
CSRF_COOKIE_PATH = '/'
CSRF_COOKIE_AGE = 31449600  # 1 año
CSRF_COOKIE_SAMESITE = 'Lax'

SESSION_COOKIE_SAMESITE = 'Lax'

if ENVIRONMENT == 'production':
    DEBUG = False

    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True

    ALLOWED_HOSTS = [
        'tecitostore.com',
        'api.tecitostore.com',
        '179.43.127.60',
        'www.tecitostore.com',
        '172.18.0.4:8000',
    ]

    CORS_ALLOW_ORIGINS = [
        'https://tecitostore.com',
        'https://api.tecitostore.com',
        'https://www.tecitostore.com',
    ]

    CORS_ALLOWED_ORIGINS = CORS_ALLOW_ORIGINS

    CSRF_COOKIE_SECURE = True
    CSRF_COOKIE_HTTPONLY = True
    CSRF_COOKIE_DOMAIN = '.tecitostore.com'
    CSRF_TRUSTED_ORIGINS = [
        'http://localhost:3000',
        'https://localhost:8081',
        'http://localhost:8000',
        'https://tecitostore.com',
        'https://api.tecitostore.com',
        'https://www.tecitostore.com',
    ]

    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_BROWSER_XSS_FILTER = True

    X_FRAME_OPTIONS = 'DENY'

    CORS_ALLOWED_ORIGIN_REGEXES = [
        r'^https://tecitostore\.com$',
        r'^https://www\.tecitostore\.com$',
        r'^https://api\.tecitostore\.com$',
    ]

else:
    DEBUG = True

    ALLOWED_HOSTS = ['*']

    CORS_ALLOWED_ORIGINS = [
        'http://localhost:3000',
        'http://localhost:8000',
        'exp://192.168.0.24:8081',
    ]

    CSRF_COOKIE_SECURE = False
    CSRF_COOKIE_HTTPONLY = False
    CSRF_COOKIE_DOMAIN = None

    CSRF_TRUSTED_ORIGINS = [
        'http://localhost:3000',
        'http://localhost:8000',
        'exp://192.168.0.24:8081',
    ]

    SECURE_SSL_REDIRECT = False
    SECURE_HSTS_SECONDS = 0
    SECURE_HSTS_INCLUDE_SUBDOMAINS = False
    SECURE_HSTS_PRELOAD = False
    SECURE_CONTENT_TYPE_NOSNIFF = False
    X_FRAME_OPTIONS = 'ALLOW'
    CONTENT_SECURITY_POLICY = ''
    SECURE_BROWSER_XSS_FILTER = False
    SESSION_COOKIE_SECURE = False
    SESSION_COOKIE_HTTPONLY = False

CORS_ORIGIN_WHITELIST = CORS_ALLOWED_ORIGINS
