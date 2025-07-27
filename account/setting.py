import os
from pathlib import Path

#

BASE_DIR = Path(__file__).resolve().parent.parent

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Tambahkan LOGIN_URL di bawah sini:
LOGIN_URL = '/login/'
ALLOWED_HOSTS = ['54.206.150.159', 'localhost','*' ]


# Static files
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'account/static'),
]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')


# Login URL
LOGIN_URL = '/login/'

