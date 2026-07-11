"""
Django settings for uevent project.
"""
import os
from pathlib import Path
from django.urls import reverse_lazy
import dj_database_url


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-o+%rww)m56b*!v9cisbm#^g3tx2-+n!lzuz4tmdkm=e@r00wg%')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', 'True') == 'True'

# ALLOWED_HOSTS
ALLOWED_HOSTS = ['*'] if DEBUG else os.environ.get('ALLOWED_HOSTS', '').split(',')

# เพิ่ม Railway domains
if os.environ.get('RAILWAY_ENVIRONMENT'):
    ALLOWED_HOSTS.append('.railway.app')


# Application definition

INSTALLED_APPS = [
    "unfold",  # ใส่บรรทัดนี้
    "unfold.contrib.filters",  # ถ้าอยากได้ตัวกรองสวยๆ
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    ##'django.contrib.staticfiles',
    'django_filters',
    'django_rest_passwordreset',

    # เก็บรูปภาพบน server
    'cloudinary_storage',
    'django.contrib.staticfiles',
    'cloudinary',
    
    # Third-party apps
    'rest_framework',
    'corsheaders',
    
    # Local apps
    'users',
    'activities',
    'news',
    'notifications',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # สำหรับ serve static files
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'uevent.urls'

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

WSGI_APPLICATION = 'uevent.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

# ใช้ PostgreSQL จาก Railway ถ้ามี DATABASE_URL
if os.environ.get('DATABASE_URL'):
    DATABASES = {
        'default': dj_database_url.config(
            default=os.environ.get('DATABASE_URL'),
            conn_max_age=600,
            conn_health_checks=True,
        )
    }
else:
    # ใช้ Local PostgreSQL สำหรับ Development
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'uevent_dev',
            'USER': 'postgres',
            'PASSWORD': 'Focus13121',
            'HOST': 'localhost',
            'PORT': '5432',
        }
    }


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'th-th'
TIME_ZONE = 'Asia/Bangkok'

USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Whitenoise configuration
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media Files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# CORS Settings
if DEBUG:
    CORS_ALLOWED_ORIGINS = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ]
else:
    # สำหรับ Production - อนุญาต Railway domains
    cors_origins = os.environ.get('CORS_ALLOWED_ORIGINS', '')
    if cors_origins:
        CORS_ALLOWED_ORIGINS = cors_origins.split(',')
    else:
        CORS_ALLOW_ALL_ORIGINS = True  # หรือระบุ frontend URL

CORS_ALLOW_CREDENTIALS = True

# REST Framework Settings
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.MultiPartParser',
        'rest_framework.parsers.FormParser',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}

# Email Backend Settings
if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    # ใช้ SMTP จริงใน production
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.gmail.com')
    EMAIL_PORT = int(os.environ.get('EMAIL_PORT', '587'))
    EMAIL_USE_TLS = True
    EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
    EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')

# Security Settings for Production
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'


# settings.py

UNFOLD = {
    "SITE_TITLE": "UEvent Admin",
    "SITE_HEADER": "UEvent Management",
    "SITE_URL": "/",
    "SIDEBAR": {
        "show_search": True,
        "show_all_applications": False,
        "navigation": [
            {
                "title": "การจัดการผู้ใช้",
                "separator": True,
                "items": [
                    {
                        "title": "โปรไฟล์ผู้ใช้",
                        "icon": "account_circle",
                        # 👈 2. ใส่ reverse_lazy() ครอบชื่อลิงก์
                        "link": reverse_lazy("admin:users_userprofile_changelist"), 
                    },
                    {
                        "title": "บัญชีระบบ (Users)",
                        "icon": "manage_accounts",
                        "link": reverse_lazy("admin:auth_user_changelist"),
                    },
                    {
                        "title": "กลุ่มผู้ดูแล (Groups)",
                        "icon": "groups",
                        "link": reverse_lazy("admin:auth_group_changelist"),
                    },
                ],
            },
            {
                "title": "กิจกรรมและข่าวสาร",
                "separator": True,
                "items": [
                    {
                        "title": "กิจกรรมทั้งหมด",
                        "icon": "event_available",
                        # ⚠️ เช็คชื่อ Model ให้ชัวร์นะครับ (activity หรือ activities)
                        "link": reverse_lazy("admin:activities_activity_changelist"), 
                    },
                    {
                        "title": "การลงทะเบียน",
                        "icon": "how_to_reg",
                        "link": reverse_lazy("admin:activities_registration_changelist"),
                    },
                    {
                        "title": "ข่าวประชาสัมพันธ์",
                        "icon": "newspaper",
                        "link": reverse_lazy("admin:news_news_changelist"),
                    },
                ],
            },
            {
                "title": "ข้อมูลระบบ",
                "separator": True,
                "items": [
                    {
                        "title": "แท็ก (Tags)",
                        "icon": "label",
                        "link": reverse_lazy("admin:activities_tag_changelist"),
                    },
                    {
                        "title": "ความสนใจ (Interests)",
                        "icon": "favorite",
                        "link": reverse_lazy("admin:activities_userinterest_changelist"),
                    },
                ],
            },
        ],
    },
} 


DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.environ.get('twnq2lm6'),
    'API_KEY': os.environ.get('992537753363962'),
    'API_SECRET': os.environ.get('JPap7KdD_T4sZELy9BpDHth9BEU')
}