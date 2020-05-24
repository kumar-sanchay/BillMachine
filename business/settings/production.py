from .base import *

DEBUG = False

ADMINS = (
    ('Sanchay Kumar', 'dsanchaykumar@gmail.com'),
)

ALLOWED_HOSTS = ['billmachine.com', 'www.billmachine.com']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'business_app',
        'USER': 'sanchay',
        'PASSWORD': 'sunnykumar123?',
    }
}