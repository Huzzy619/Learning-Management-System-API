from .settings import *
import os 
# import dj_database_url

SECRET_KEY = os.environ.get('SECRET_KEY', SECRET_KEY)

DEBUG = False

ALLOWED_HOSTS = ['lms.up.railway.app']

CSRF_TRUSTED_ORIGINS = ['https://lms.up.railway.app']

# DATABASES = {
#     "default": dj_database_url.config()
# }

INSTALLED_APPS.remove("playground")

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.environ['CLOUD_NAME'],
    'API_KEY': os.environ['CLOUD_API_KEY'],
    'API_SECRET': os.environ['CLOUD_API_SECRET'],
}


EMAIL_HOST = 'smtp.mailtrap.io'
EMAIL_HOST_USER = '617e747e2afc2c'
EMAIL_HOST_PASSWORD = 'e99890b04db43b'
EMAIL_PORT = '2525'


CELERY_BROKER_URL = 'redis://localhost:6379/1'

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        # For each OAuth based provider, either add a ``SocialApp``
        # (``socialaccount`` app) containing the required client
        # credentials, or list them here:
        'APP': {
            'client_id': '878674025478-e8s4rf34md8h4n7qobb6mog43nfhfb7r.apps.googleusercontent.com',
            'secret': os.environ.get('GOOGLE_SECRET'),
            'key': ''
        },

        'SCOPE': [
            'profile',
            'email',
        ],

        'AUTH_PARAMS': {
            'access_type': 'online',
        },
    }
}