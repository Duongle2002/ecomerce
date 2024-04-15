'''
Django settings for fruitables project.

Generated by 'django-admin startproject' using Django 4.2.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
'''

from datetime import timedelta
import os
from pathlib import Path
import cloudinary.api
from decouple import config
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=True, cast=bool)



# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'fruitables',
    'products',
    'rest_framework',
    'cloudinary',
    'upload',
    'rest_framework.authtoken',
    'djoser',
    'user',
    'orders',
    'drf_yasg',
    "whitenoise.runserver_nostatic",
    'corsheaders',
    'homeapp' ,
    'cart',
    'django.contrib.humanize',
    'introduce',
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
    'corsheaders.middleware.CorsMiddleware',
    
    
]

ROOT_URLCONF = 'fruitables.urls'

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
                'cart.context_processors.cart_items',
            ],
        },
    },
]

WSGI_APPLICATION = 'fruitables.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
import dj_database_url
DATABASES = {
    'default': dj_database_url.parse(config('DATABASE_URL'), conn_max_age=600, conn_health_checks=True)
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators
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
# https://docs.djangoproject.com/en/4.2/topics/i18n/
LANGUAGES = [
    ('en', 'English'),
    ('vi', 'Tiếng Việt'),
]

TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# Cloudinary Configuration
cloudinary.config(
    cloud_name=config("CLOUDINARY_CLOUD_NAME"),
    api_key=config("CLOUDINARY_API_KEY"),
    api_secret=config("CLOUDINARY_API_SECRET"),
)

# Rest Framework Settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAdminUser',
        'rest_framework.permissions.IsAuthenticated',
        'rest_framework.permissions.AllowAny',
    ),
}

# JWT Settings
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=30),
}

# DJOSER Settings
DJOSER = {
    'SEND_ACTIVATION_EMAIL': False,
}

# Custom User Model
AUTH_USER_MODEL = 'user.UserAccount'

# Swagger Settings
SWAGGER_SETTINGS = {
    'USE_SESSION_AUTH': False
}

# Whitenoise Storage Settings

# Corsheaders Configuration
# Whitenoise Storage Settings
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


from decouple import config

# Lấy giá trị môi trường ALLOWED_HOSTS từ biến môi trường và chuyển đổi thành danh sách các host được phép
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1', cast=lambda v: [s.strip() for s in v.split(',')])

# Lấy giá trị môi trường CORS_ALLOWED_ORIGINS từ biến môi trường và chuyển đổi thành danh sách các origin được phép
CORS_ALLOWED_ORIGINS = config('CORS_ALLOWED_ORIGINS', default='http://localhost:3000', cast=lambda v: [s.strip() for s in v.split(',')])

# Lấy giá trị môi trường CORS_ALLOW_ALL_ORIGINS từ biến môi trường và chuyển đổi thành kiểu boolean
CORS_ALLOW_ALL_ORIGINS = config('CORS_ALLOW_ALL_ORIGINS', default=False, cast=bool)

# Thêm địa chỉ IP tĩnh vào danh sách ALLOWED_HOSTS
ALLOWED_HOSTS += ['100.20.92.101']

# Thêm địa chỉ IP tĩnh vào danh sách CORS_ALLOWED_ORIGINS


# Nếu bạn muốn cho phép tất cả các origin, hãy sử dụng CORS_ALLOW_ALL_ORIGINS
if CORS_ALLOW_ALL_ORIGINS:
    CORS_ALLOWED_ORIGINS = ['*']
CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
    'http://100.20.92.101',  # Thêm địa chỉ IP tĩnh vào danh sách
]