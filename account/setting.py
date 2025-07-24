import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Tambahkan LOGIN_URL di bawah sini:
LOGIN_URL = '/login/'
