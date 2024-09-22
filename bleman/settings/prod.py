from .common import *
import os
import dj_database_url

SECRET_KEY = os.environ['SECRET_KEY']
DEBUG = False

DATABASES = {
    'default': dj_database_url.config()
}

ALLOWED_HOSTS = ['bleman.fly.dev']
