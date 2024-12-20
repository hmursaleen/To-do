"""
Django settings for todo project.

Generated by 'django-admin startproject' using Django 5.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-@hh^d39ogc=svcbi!nq4rvc!z%aef_v)0h-!v_kpt_9&56&far'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'tasks.apps.TasksConfig',
    'api.apps.ApiConfig',
    'users.apps.UsersConfig',
    'notifications.apps.NotificationsConfig',
    'core.apps.CoreConfig',
    'search.apps.SearchConfig',
    'teams.apps.TeamsConfig',

    'rest_framework',
    'drf_yasg',
    'corsheaders',
    'channels',
    
]

'''
    CORS Headers: If your API will be consumed by external frontend applications (e.g., React or Vue.js), consider installing and configuring django-cors-headers to allow cross-origin resource sharing:
'''
'''
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",  # Example for React app
    "http://localhost:8000",  # Example for Vue app
    "http://yourdomain.com",  # Add your production domain here
]
'''
## Allow all domains to make requests to your API (adjust as necessary)
CORS_ALLOW_ALL_ORIGINS = True #


# Celery configuration

CELERY_BROKER_URL = 'redis://localhost:6379/0'  # Redis broker URL
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'  # Redis result backend
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Dhaka'


# Celery Beat for periodic tasks
CELERY_BEAT_SCHEDULE = {
    'check_deadline_tasks': {
        'task': 'tasks.tasks.check_upcoming_deadlines',
        'schedule': 180.0,  # Run every hour
    },
}


CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('127.0.0.1', 6379)],  # or your Redis host and port
        },
    },
}

#CHANNEL_LAYERS: Configures the channel layer with Redis as the backend.


REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',  # API will use JSON responses by default
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',  # Parse JSON requests
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',  # For session-based authentication
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',  # Default permission for all views
    ],
    #'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.CursorPagination',
    'PAGE_SIZE': 10,  # Number of items per page
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',  # For auto-generating API schemas

    # Throttling: Implement throttling to prevent abuse of your API.
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.UserRateThrottle',
        'rest_framework.throttling.AnonRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'user': '100/day',
        'anon': '10/hour',
    },
}


'''
DEFAULT_RENDERER_CLASSES: Limits the responses to JSON (though you can add other formats like BrowsableAPIRenderer).
DEFAULT_PARSER_CLASSES: Handles incoming JSON data.
DEFAULT_AUTHENTICATION_CLASSES: Sets the default authentication method (session-based for now).
DEFAULT_PERMISSION_CLASSES: Enforces IsAuthenticated globally to restrict access to authenticated users (you can override it on individual views).
Pagination: The PageNumberPagination class is set for paginating API results with 10 items per page.
'''

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware'
]

ROOT_URLCONF = 'todo.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        
        'DIRS': [os.path.join(BASE_DIR, 'templates')],  # Add your centralized templates directory here
        'APP_DIRS': True,  # Enable this to allow loading templates from within apps

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

WSGI_APPLICATION = 'todo.wsgi.application'

ASGI_APPLICATION = 'todo.asgi.application'

#ASGI_APPLICATION: This setting points to the asgi.py file where the Channels setup resides

#ASGI_APPLICATION = 'todo.routing.application'




# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

'''
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
'''

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'todo_project',  # Your database name
        'USER': 'todo_user',  # Your database user
        'PASSWORD': 'admin',  # Your user's password
        'HOST': 'localhost',  # Default host
        'PORT': '5432',  # Default port
    }
}


'''
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://localhost:6379/1',  # 1 is the database number
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        },
    }
}
'''

# Optional: To speed up sessions, you can use Redis as the session backend
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"



# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'habibulmursaleen@gmail.com'
EMAIL_HOST_PASSWORD = 'qfmw txsw dtec ovmq'
DEFAULT_FROM_EMAIL = 'habibulmursaleen@gmail.com'


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Dhaka'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

'''
You can use the default User model from Django (django.contrib.auth.models.User) if no customization is needed. If you want to extend the User model in the future (e.g., for profiles or custom fields), plan to use a Custom User Model.

For now, stick to Django's default User model:
'''
AUTH_USER_MODEL = 'auth.User'


LOGIN_REDIRECT_URL = 'tasks:task-list'  # Redirect to task list after login
LOGOUT_REDIRECT_URL = 'users:login'     # Redirect to login after logout
