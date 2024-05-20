import os

from dotenv import load_dotenv
from jelly_backend.settings import *

load_dotenv()

DEBUG = True

allowed_hosts = [
    'localhost',
    '127.0.0.1'
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('NAME_DEV'),
        'USER': os.getenv('USER_DEV'),
        'PASSWORD': os.getenv('PASSWORD_DEV'),
        'HOST': os.getenv('HOST_DEV'),
        'PORT': '5432',
    }
}
