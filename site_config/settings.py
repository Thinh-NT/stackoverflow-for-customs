from pathlib import Path
import os
import datetime
from django.conf import settings
import logging.config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-(fq75niz3o802+k42y*4$@8!_(uywr6qwnv#c&2m!%8zdq+8$q'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*', '192.168.1.69', '192.168.1.96']


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    'channels',
    'notifications',

    # local
    'posts',

    # 3rd apps
    'drf_yasg',

    # Auth
    'corsheaders',
    'accounts',
    'djoser',
    'rest_framework_simplejwt',

    'rest_framework',

    # Delete when production,
    'nplusone.ext.django',
]

SITE_ID = 1

CORS_ORIGIN_ALLOW_ALL = True

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # Delete when production
    'nplusone.ext.django.NPlusOneMiddleware',
]
MIDDLEWARE += ('debug_toolbar.middleware.DebugToolbarMiddleware',)

NPLUSONE_LOGGER = logging.getLogger('nplusone')
NPLUSONE_LOG_LEVEL = logging.WARN

SERVER_EMAIL = 'thanhthinhkrb@gmail.com'
ADMINS = [
    ('thinhnt', 'thanhthinhkrb@gmail.com'),
]
MANAGERS = ADMINS

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True
        },
        'logfile': {
            'class': 'logging.handlers.WatchedFileHandler',
            'filename': BASE_DIR / 'uni.log'
        },
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        'nplusone': {
            'handlers': ['console'],
            'level': 'WARN',
        },
    }
}

ROOT_URLCONF = 'site_config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'frontend/build'],
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

WSGI_APPLICATION = 'site_config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'stack_uni',
        'HOST': os.environ.get('MYSQL_DBHOST'),
        'PORT': os.environ.get('MYSQL_DBPORT'),
        'USER': os.environ.get('MYSQL_DBUSER'),
        'PASSWORD': os.environ.get('MYSQL_DBPASS'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    # {
    #     'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    # },
]

SERVER_EMAIL = 'thanhthinhkrb@gmail.com'
ADMINS = [
    ('thinhnt', 'thanhthinhkrb@gmail.com'),
]
MANAGERS = ADMINS

# EMAIL CONFIG
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
MEDIA_URL = '/media/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'frontend/build/static'),
]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': ['rest_framework.permissions.AllowAny'],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 10
}

# SIMPLE_JWT = {
#     'AUTH_HEADER_TYPES': ('Bearer',),
#     "ACCESS_TOKEN_LIFETIME": datetime.timedelta(days=7),
#     "REFRESH_TOKEN_LIFETIME": datetime.timedelta(days=14),
#     "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
# }

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': datetime.timedelta(days=14),
    'REFRESH_TOKEN_LIFETIME': datetime.timedelta(days=25),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': False,
    'UPDATE_LAST_LOGIN': False,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    'JWK_URL': None,
    'LEEWAY': 0,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': datetime.timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': datetime.timedelta(days=1),
}


# DJOSER CONFIG
AUTH_USER_MODEL = 'accounts.User'


DJOSER = {
    "LOGIN_FIELD": "email",
    "USER_CREATE_PASSWORD_RETYPE": True,
    "USERNAME_CHANGED_EMAIL_CONFIRMATION": True,
    "PASSWORD_CHANGED_EMAIL_CONFIRMATION": True,
    "SEND_CONFIRMATION_EMAIL": False,
    "SET_USERNAME_RETYPE": True,
    "SET_PASSWORD_RETYPE": True,
    "USERNAME_RESET_CONFIRM_URL": "password/reset/confirm/{uid}/{token}",
    "PASSWORD_RESET_CONFIRM_URL": "email/reset/confirm/{uid}/{token}",
    "ACTIVATION_URL": "activate/{uid}/{token}",
    "SEND_ACTIVATION_EMAIL": False,
    "SOCIAL_AUTH_TOKEN_STRATEGY": "djoser.social.token.jwt.TokenStrategy",
    "SERIALIZERS": {
        "user_create": "accounts.serializers.UserCreateSerializer",  # custom serializer
        "user": "djoser.serializers.UserSerializer",
        "current_user": "accounts.serializers.UniUserSerializer",
        "user_delete": "djoser.serializers.UserSerializer",
    },
    # "SOCIAL_AUTH_ALLOWED_REDIRECT_URIS": [
    #     "your redirect url",
    #     "your redirect url",
    # ],
}

# CORS HEADERS
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True

# Django Channels
# your_project_name.routing.application
ASGI_APPLICATION = "notifications.routing.application"

# Adding Django Channel Layers
redis_host = [{
    # don't miss the 'rediss'!
    'address': f'rediss://{os.environ["REDIS_PASSWORD"]}@192.168.1.99:6379',
}]
CHANNEL_LAYERS = {
    'default': {
        # Method 1: Via redis lab
        # "BACKEND": "channels_redis.core.RedisChannelLayer",
        # "CONFIG": {
        #     "hosts": redis_host,
        # },

        # "BACKEND": "channels_redis.core.RedisChannelLayer",
        # "CONFIG": {
        #     "hosts": [f"redis://:{os.environ['REDIS_PASSWORD']}@192.168.1.99/0"],
        #     "symmetric_encryption_keys": [SECRET_KEY],
        # },

        # Method 2: Via In-memory channel layer
        # Using this method.
        "BACKEND": "channels.layers.InMemoryChannelLayer"
    },
}
