from .common import *
import os

SECRET_KEY = os.environ['SECRET_KEY']
DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'bleman.fly.dev']

CSRF_TRUSTED_ORIGINS = ['https://bleman.fly.dev']
