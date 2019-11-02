"""
Django settings for nzemn1 project.

Generated by 'django-admin startproject' using Django 2.2.4.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import json
import os
from django.core.exceptions import ImproperlyConfigured

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Import 'secret' info
if (os.path.isfile(os.path.join(BASE_DIR, 'secrets.json'))):
    with open(os.path.join(BASE_DIR, 'secrets.json')) as secrets_file:
        secrets = json.load(secrets_file)
else:
    secrets = {
      "SECRET_KEY": "default",
      "USER": "user",
      "DB_PASSWORD": "pass"
    }

def get_secret(setting, secrets=secrets):
    """Get secret setting or fail with ImproperlyConfigured"""
    try:
        return secrets[setting]
    except KeyError:
        raise ImproperlyConfigured("Set the {} setting".format(setting))



# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = get_secret('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    #'sites.apps.SitesConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',
    'sites',
    'leaflet',
    'guardian',
    'rest_framework',
    'rest_framework_gis'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'mon-site-register.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'mon-site-register.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        # Initial SQLite database
        #'ENGINE': 'django.db.backends.sqlite3',
        #'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),

        # Updated to PostGIS
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'gisdb',
        'USER': get_secret('USER'),
        'PASSWORD': get_secret('DB_PASSWORD'),
        'HOST':'localhost',
        'PORT':'5433',

    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Pacific/Auckland'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'

# For Heroku
GDAL_LIBRARY_PATH = os.environ.get('GDAL_LIBRARY_PATH')
GEOS_LIBRARY_PATH = os.environ.get('GEOS_LIBRARY_PATH')

# Leaflet Configurations
LEAFLET_CONFIG = {
    'DEFAULT_CENTER': (-41.2706, 173.2840),
    'DEFAULT_ZOOM': 5,
    'MAX_ZOOM': 20,
    'MIN_ZOOM':3,
    'SCALE': 'both',
    'ATTRIBUTION_PREFIX': 'Inspired by Life in GIS'
}

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend', # this is default
    'guardian.backends.ObjectPermissionBackend',
)

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ],
    #'DEFAULT_RENDERER_CLASSES': [
    #    'rest_framework.renderers.JSONRenderer',
    #    'rest_framework.renderers.AdminRenderer',
    #    'rest_framework.renderers.TemplateHTMLRenderer',
    #]
}

# Configure Django App for Heroku.
import django_heroku
django_heroku.settings(locals())
