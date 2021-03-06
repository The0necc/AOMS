"""
Django settings for AOMS project.

Generated by 'django-admin startproject' using Django 1.11.9.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'zh_f$q@_u01)804t=vrfb-p2k60p*j3hh(lce6rim5(!vyaz-o'

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
    'rest_framework',
    'web_home.apps.WebHomeConfig',
    'web_cmdb.apps.WebCmdbConfig',
    'web_api.apps.WebApiConfig',
    'web_cmdb.templatetags'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'web_cmdb.middlewares.rbac.RbacMiddleWare'
]

ROOT_URLCONF = 'AOMS.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
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

WSGI_APPLICATION = 'AOMS.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'aoms',
        'USER': 'root',
        'PASSWORD': 'root@123',
        'HOST': '127.0.0.1',
        'PORT': '3306',
        },
    'web_cmdb': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'web_cmdb',
        'USER': 'root',
        'PASSWORD': 'root@123',
        'HOST': '127.0.0.1',
        'PORT': '3306',
        }
}
# DATABASE_ROUTERS = [.db_router.appinfoRouter]
DATABASE_ROUTERS = ['AOMS.db_router.DatabaseAppsRouter']
DATABASE_APPS_MAPPING = {
    # example:
    # 'app_name':'database_name',
    'web_cmdb': 'web_cmdb',
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]


# rbac白名单
RBAC_WHILE_URL = [
    r'^/login/$',r'^/logout/$',r'^/admin/',r'^/api/',
]

#rbac免认证名单
RBAC_PASS_URL = [
    r'^/home/$',r'^/api/',
]

# rest_framework 配置文件
REST_FRAMEWORK = {
    "ALLOWED_VERSIONS":['v1','v2'],
    # "DEFAULT_VERSIONING_CLASS":"rest_framework.versioning.URLPathVersioning",
}

# 资产入库配置文件
CMDB_PLUGINS_DICT = {
    'disk':"web_api.plugins.disk.Disk",
    'cpu':"web_api.plugins.cpu_and_board.CPUAndBoard",
    'board':"web_api.plugins.cpu_and_board.CPUAndBoard",
    'memory':"web_api.plugins.memory.Memory",
}