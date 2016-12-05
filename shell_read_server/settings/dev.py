# -*- coding: utf-8 -*-

from .base import *

DEBUG = True

# ALLOWED_HOSTS = [
#     "localhost",
# ]

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#         # 'OPTIONS': {'charset': 'utf8'},
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'shell_read',
        'USER': 'root',
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
