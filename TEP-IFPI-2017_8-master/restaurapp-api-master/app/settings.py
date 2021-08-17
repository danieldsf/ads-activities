import os, dj_database_url
from unipath import Path
from decouple import config
from raven import Client

BASE_DIR = Path(__file__).parent

SECRET_KEY = config('SECRET_KEY', default='Brazil1x7Germany', cast=str)

AUTH_USER_MODEL = 'core.user'

PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.MD5PasswordHasher',
)

DEBUG = config('DEBUG', default=False, cast=bool)

TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = ('*',)

# Email settings

DEFAULT_FROM_EMAIL = 'Restaurapp <admin@restaurapp.com>'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'  # During development only

# Static files (CSS, JavaScript, Images)

STATIC_URL  = '/static/'

MEDIA_URL   = '/media/'

STATIC_ROOT = BASE_DIR.parent.child('static')

MEDIA_ROOT  = BASE_DIR.parent.child('media')

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
    'oauth2_provider',
    'corsheaders',
    'rest_framework.authtoken',
    'rest_framework_swagger',
    'django_rest_passwordreset',
    'raven.contrib.django.raven_compat',
]



MIDDLEWARE = [
    #Extra Middlewares:
    'corsheaders.middleware.CorsMiddleware',
    
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
            ],
        },
    },
]

WSGI_APPLICATION = 'app.wsgi.application'

# Database + Error Tracking

DATABASES = {}

client = None

if config('IS_TRAVIS', default=False, cast=bool):
    DATABASES['default'] = dj_database_url.parse('sqlite:///' + BASE_DIR.child('db.sqlite3'))
else:
    # EMAIL:
    EMAIL_HOST = config('EMAIL_HOST', default=os.environ.get('EMAIL_HOST'), cast=str)
    EMAIL_PORT = config('EMAIL_PORT', default=os.environ.get('EMAIL_PORT'), cast=int)
    EMAIL_HOST_USER = config('EMAIL_HOST_USER', default=os.environ.get('EMAIL_HOST_USER'), cast=str)
    EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default=os.environ.get('EMAIL_HOST_PASSWORD'), cast=str)
    EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=os.environ.get('EMAIL_USE_TLS'), cast=bool)

    # Raven Settings:
    client = Client(config('RAVEN_DSN', default=os.environ.get('RAVEN_DSN'), cast=str))
    DATABASES['default'] = dj_database_url.parse(config('DATABASE_URL', default=os.environ.get('DATABASE_URL'), cast=str), conn_max_age=600)    

# Password validation

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Fortaleza'

USE_I18N  = USE_L10N  = USE_TZ    = True

DEFAULT_CHARSET = 'utf-8'

# CORS:

CORS_ORIGIN_ALLOW_ALL = True

REST_FRAMEWORK = {
    'PAGE_SIZE': 10,
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
    ),
    'DEFAULT_THROTTLE_CLASSES': (
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
    ),
    'DEFAULT_THROTTLE_RATES': {
        'obtain-token-jwt': '10000/hour',
        'obtain-token-oauth2': '10000/hour',
        'anon': '60/hour',
        'user': '600/hour',
    },
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
    'TEST_REQUEST_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.TemplateHTMLRenderer',
    ),
}