from .common import *

SECRET_KEY = 'django-insecure-8lk0c_(m(kwygwalgfnw^b8*9!-u^etgk%2&=4c%&ih(xmwb7n'
DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
