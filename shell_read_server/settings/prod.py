# -*- coding: utf-8 -*-

from .base import *  # noqa

DEBUG = False

ALLOWED_HOSTS = [
    "localhost",
    "shell_read.leonornot.org",
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'database',
        'USER': 'username',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': 3306,
        'OPTIONS': {'charset': 'utf8'},
    }
}

REDIS = {
    "host": "localhost",
    "port": 6379,
}
