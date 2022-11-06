from .settings import *
import os 
import dj_database_url

SECRET_KEY = os.environ.get('SECRET_KEY', SECRET_KEY)

DEBUG = False

ALLOWED_HOSTS = []

CSRF_TRUSTED_ORIGINS = ['https://portfolio-production-6724.up.railway.app']

DATABASES = {
    "default": dj_database_url.config()
}

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.environ['CLOUD_NAME'],
    'API_KEY': os.environ['CLOUD_API_KEY'],
    'API_SECRET': os.environ['CLOUD_API_SECRET'],
}


EMAIL_USER = ""
EMAIL_PASSWORD = ""
EMAIL_HOST = "localhost"
EMAIL_PORT = 2525


CELERY_BROKER_URL = 'redis://localhost:6379/1'