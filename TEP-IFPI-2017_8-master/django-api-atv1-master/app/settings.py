import os, raven, logging
from unipath import Path
from decouple import config

BASE_DIR = Path(__file__).parent
PROJECT_DIR = BASE_DIR.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY', default=os.environ.get('SECRET_KEY'), cast=str)

LOGIN_URL = '/login/'
LOGOUT_URL = '/logout/'
LOGIN_REDIRECT_URL = '/'

PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.MD5PasswordHasher',
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = ('*',)
INTERNAL_IPS  = ('127.0.0.1','192.168.0.1','localhost')

# Email settings

EMAIL_HOST = config('EMAIL_HOST', default=os.environ.get('EMAIL_HOST'), cast=str)
EMAIL_PORT = config('EMAIL_PORT', default=os.environ.get('EMAIL_PORT'), cast=int)
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default=os.environ.get('EMAIL_HOST_USER'), cast=str)
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default=os.environ.get('EMAIL_HOST_PASSWORD'), cast=str)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=os.environ.get('EMAIL_USE_TLS'), cast=bool)
DEFAULT_FROM_EMAIL = 'StudentMy Team <admin@studentmy.com>'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'  # During development only

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL  = '/static/'
STATIC_ROOT = BASE_DIR.parent.child('static')

# Application definition
INSTALLED_APPS = [
    'rest_framework',
    'django.contrib.auth',
    'core',
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles', 
    # Extra Apps:
    'raven.contrib.django.raven_compat',
]

IMPORT_EXPORT_USE_TRANSACTIONS = True

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                #Extra context processors:

                #'django.core.context_processors.i18n',
            ],
        },
    },
]

WSGI_APPLICATION = 'app.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Fortaleza'
USE_I18N  = True
USE_L10N  = True
USE_TZ    = True

DEFAULT_CHARSET = 'utf-8'

LOCALE_PATHS = (
    BASE_DIR.child('locale'),
)

MEDIA_URL   = '/media/'
MEDIA_ROOT  = BASE_DIR.parent.child('media')

STATICFILES_DIRS = (
    BASE_DIR.parent.child('node_modules'),
    STATIC_ROOT.child('custom'),
)

# BASE_DIR.parent.child('static'),

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# Raven Settings:

RAVEN_CONFIG = {
    'dsn': config('RAVEN_DSN', default=os.environ.get('RAVEN_DSN'), cast=str),
    #'release': raven.fetch_git_sha(BASE_DIR.child('.git').child('HEAD')),
}