from jelly_backend.settings import *

DEBUG = False

ALLOWED_HOSTS = [
    'mi-dominio.com',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'nombre_basededatos',
        'USER': 'usuario_basededatos',
        'PASSWORD': 'contraseña_basededatos',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

