"""
Django settings for agency project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
PROJECT_DIR = os.path.dirname(os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '=c3v1$)^86^(m)h@2--h)q3vbx@%3f-c(v=7%2(ddj0ynl_s%b'

AWS_ACCESS_KEY_ID = 'AKIAIADEAKOANSKRCTGQ'
AWS_SECRET_ACCESS_KEY = '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'

AWS_STORAGE_BUCKET_NAME = 'uploads.bienfacile.com'
AWS_S3_REGION_NAME = 'eu-west-3'
AWS_S3_ENDPOINT_URL = 'https://s3-eu-west-3.amazonaws.com'

S3DIRECT_DESTINATIONS = {
    'uploads': {
        'key': lambda filename, args: args + '/' + filename,
        'key_args': 'uploads',
        'content_disposition': lambda x: 'attachment; filename="{}"'.format(x),
        'content_length_range': (1000, 20000000),
    }
}


# SECURITY WARNING: don't run with debug turned on in production!
SITE_URLS = { 'DEV' : 'http://192.168.1.72:8000', 'STAGING' : 'https://staging.bienfacile.com', 'LIVE' : 'https://agence.bienfacile.com' }

SERVER_ENVIRONMENT = os.environ['SERVER_ENVIRONMEMT'] if 'SERVER_ENVIRONMEMT' in os.environ else 'LIVE'

#SERVER_ENVIRONMENT = 'DEV'

DEBUG = True if SERVER_ENVIRONMENT != 'LIVE' else False

SITE_URL = SITE_URLS[SERVER_ENVIRONMENT]

LOGGING_CONFIG = None

SETTINGS_EXPORT = [
    'DEBUG',
    'MEDIA_URL',
    'SERVER_ENVIRONMENT',
    'SITE_URL',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': False,
        'DIRS': ['agents/templates','venv/lib/python2.7/site-packages/django/contrib/admin/templates'],
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django_settings_export.settings_export',
                'django.template.context_processors.request'
            ],
        },
    },
]

ALLOWED_HOSTS = [ 'agence.bienfacile.com', 'staging.bienfacile.com', 'demo.bienfacile.com', '0.0.0.0', '127.0.0.1', '192.168.1.76', ]



# Application definition

INSTALLED_APPS = (
    'grappelli',
    'widget_tweaks',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'user_sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'oauth2_provider',
    'corsheaders',
    's3direct',
    'agents',
    'notaires',
    'clients',
    'todo',
    'chat',
    'news',
    'sales',
    'simulations',
    'files',
    'finance',
)

MIDDLEWARE_CLASSES = (
    'user_sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'oauth2_provider.middleware.OAuth2TokenMiddleware',
    'django_user_agents.middleware.UserAgentMiddleware',
#    'agency.MobileMiddleware.MobileMiddleware',
)
CORS_ORIGIN_ALLOW_ALL = True

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'oauth2_provider.backends.OAuth2Backend',
)

SESSION_ENGINE = 'user_sessions.backends.db'

SESSION_COOKIE_AGE = 2592000 # expire after 30 days

AUTH_USER_MODEL = 'agents.Agent'

GEOIP_PATH = '/home/sites/django/bienfacile/marchand/geoip/'

ROOT_URLCONF = 'agency.urls'

WSGI_APPLICATION = 'agency.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME' : 'bf_agency',
        'USER': 'bf_agency',
        'PASSWORD': 'ruz8DzFvaAeHUiHz',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Paris'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Media files - this includes file uploads

MEDIA_ROOT = '/home/sites/django/bienfacile/agency/media'
MEDIA_URL = '/media/'

# Static files (CSS, JavaScript, Images)

STATIC_ROOT = os.path.join(PROJECT_DIR, 'static')
STATIC_URL = '/static/' if DEBUG else 'https://agencystatic.bienfacile.com/'
STATICFILES_DIRS = (
    os.path.join(PROJECT_DIR, 'staticfiles'),
)
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)
