from settings import *

DEBUG = False

DEFAULT_FROM_EMAIL = 'no-reply@breslovtorah.net'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_HOST = 'mail.pawnmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = DEFAULT_FROM_EMAIL
EMAIL_HOST_PASSWORD = 'abcd4321'
EMAIL_USE_TLS = True

ALLOWED_HOSTS = ("*",)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'breslovtorah_live',                      
        'USER': 'breslovtorah_live',
        'PASSWORD': 'breslovtorah_live',
        'HOST': 'localhost'
    }
}

LOGGING['handlers']['console'] = {
    'level': 'DEBUG',
    'class': 'logging.FileHandler',
    'filename': '/home/breslovtorah/logs/live.log',
}
