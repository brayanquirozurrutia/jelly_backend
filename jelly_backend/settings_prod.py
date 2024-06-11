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
