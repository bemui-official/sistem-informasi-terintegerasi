"""
Django settings for sit_bemui project.

Generated by 'django-admin startproject' using Django 3.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
from pathlib import Path
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '%*6xd(4q!7f!$9e%ap@x(it_xr7e)zlgf%l)v1_5r*^6a_7sp9'

# Automatically determine environment by detecting if DATABASE_URL variable.
# DATABASE_URL is provided by Heroku if a database add-on is added
# (e.g. Heroku Postgres).
PRODUCTION = os.getenv('DATABASE_URL') is not None

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["sitbemui.com"]

if not PRODUCTION:
    DEBUG = True
    ALLOWED_HOSTS += ['.localhost', '127.0.0.1', '[::1]']

# Application definition

INSTALLED_APPS = [
    'linebotsit.apps.LinebotsitConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'bootstrap5',
    'advanced',
    'backend',
    'dirmawa',
    'penyetoran',
    'publikasi',
    'reimbursement',
    'sertifikat',
    'surat_keluar',
    'survei',
    'youtube',
    'user',
    'home',
    'surat_besar',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'sit_bemui.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates',
        ],
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

WSGI_APPLICATION = 'sit_bemui.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
# Set database settings automatically using DATABASE_URL.
if PRODUCTION:
    DATABASES = {
        'default': dj_database_url.config()
    }
# 'default': {
#           'ENGINE': 'django.db.backends.postgresql_psycopg2',
#           'NAME': os.getenv('DATABASE_NAME', ''),
#           'USER': os.getenv('DATABASE_USER', ''),
#           'PASSWORD': os.getenv('DATABASE_USER_PASSWORD', ''),
#           'HOST': 'localhost',
#           'PORT': '5432',
#        }
# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'

# This is the directory for storing `collectstatic` results.
# This shouldn't be included in your Git repository.
STATIC_ROOT = BASE_DIR / 'staticfiles'

# You can use this directory to store project-wide static files.
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# Enable compression and caching features of whitenoise.
# You can remove this if it causes problems on your setup.
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Line Bot Credentials
LINE_CHANNEL_ACCESS_TOKEN = 'kaPsqQV6XHaJWRR4L4I2o1Z0pGSLIEPbN5FR0YOjKrJk3pBQHLdEGZ0nzfraWJM7G63NxupKU/HLtTftejXJF9MW+y8SwKj2APq8ofKL2lmr2UGAvDGL/XSPcEncdbbGiNcKnm8UmyIWR/0Vf02irgdB04t89/1O/w1cDnyilFU='
LINE_CHANNEL_SECRET = '19a194fbe7b4f253c7398d36bc91efd6'