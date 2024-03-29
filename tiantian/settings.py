#coding=utf-8
"""
Django settings for tiantian project.

Generated by 'django-admin startproject' using Django 1.8.2.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '9dkariqo*93j1r8%9k5b7oox^5qs&d^(xoh+g$(pu0hq6)2j1$'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 'df_user',
    # 'df_goods',
    # 'cart',
    # 'tinymce',
    # 'order',
    # 'haystack',
    # 'rest_framework',
    # 'rest_framework_swagger',
    'DBcreateOrder',
    # 'drf_yasg',
    'drf_spectacular',
    'drf_spectacular_sidecar',
    'wmspda'
)

MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    # 'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    # 'tiantian.Middleware.MyLoginMiddleware',

]

ROOT_URLCONF = 'tiantian.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'template')],
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

WSGI_APPLICATION = 'tiantian.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        # 'ENGINE': 'django.db.backends.mysql',
        # 'HOST':'localhost',
        # 'PORT':'3306',
        # 'USER':'root',
        #mac mysql账号密码
        # 'PASSWORD':'zzlpython',
        # 'NAME': 'wms',
        # 公司mysql账号密码
        # 'PASSWORD': 'python',
        # 'NAME': 'ews',
    },
    'twms':{
        'ENGINE': 'django.db.backends.mysql',
        'HOST':'192.168.1.203',
        'PORT':'13306',
        'USER':'twms',
        'PASSWORD':'twms#321',
        'NAME':'twms'
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'zh-Hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True
#
# USE_L10N = True
#
# USE_TZ = True
USE_L10N = False
DATE_FORMAT = 'Y-m-d'
DATETIME_FORMAT = 'Y-m-d H:i:s'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS=[
    os.path.join(BASE_DIR,'static')
]

#本地调试使用
# MEDIA_ROOT=os.path.join(BASE_DIR,'static')
# 发布配置，本地不需要改
# MEDIA_ROOT='/var/www/tiantian/static'
#富文本配置
TINYMCE_DEFAULT_CONFIG={
    'theme':'advanced',
    'width':600,
    'height':400,
}
#配置搜索引擎
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': os.path.join(BASE_DIR, 'whoosh_index'),
    }
}
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'
HAYSTACK_SEARCH_RESULTS_PER_PAGE=10    #配置一页显示多少条数据


#p配置swagger
REST_FRAMEWORK = {
# 2、设置DEFAULT_SCHEMA_CLASS，此处不设置后续会报错。
#     'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.AutoSchema',
#新的drf_spectacular 支持swagger3.0
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema'

}

SPECTACULAR_SETTINGS = {
    'TITLE': '仓储API接口文档',
    'DESCRIPTION': '仓储造数据平台',
    'VERSION': '1.0.0',
    # OTHER SETTINGS
    #设置Swagger UI或Redoc。drf-spectacular-sidecar静态文件
    'SWAGGER_UI_DIST': 'SIDECAR',  # shorthand to use the sidecar instead
    'SWAGGER_UI_FAVICON_HREF': 'SIDECAR',
    'REDOC_DIST': 'SIDECAR',
    # OTHER SETTINGS
}
