# -*- coding: utf-8 -*-
"""
请不要修改该文件
如果你需要对settings里的内容做修改，请在config\settings_custom.py 文件中 添加即可
如有任何疑问，请联系 【蓝鲸助手】
"""
import os
import sys
# Import global settings to make it easier to extend settings.
from django.conf.global_settings import *

# ==============================================================================
# APP 运行环境配置信息
# ==============================================================================
# 此处WSGI_ENV设置用于正式环境部署
WSGI_ENV = os.environ.get("DJANGO_CONF_MODULE", "")
# 运行模式， DEVELOP(开发模式)， TEST(测试模式)， PRODUCT(正式产品模式)
RUN_MODE = 'DEVELOP'    # DEVELOP TEST PRODUCT
if WSGI_ENV.endswith("production"):
    RUN_MODE = "PRODUCT"
    DEBUG = False
elif WSGI_ENV.endswith("testing"):
    RUN_MODE = "TEST"
    DEBUG = False
else:
    RUN_MODE = "DEVELOP"
    DEBUG = True
TEMPLATE_DEBUG = DEBUG


# 加载config中的配置项
from config.settings_develop import *
from config.settings_custom import *
from config.settings_env import *

# 处理DB配置
if RUN_MODE == "TEST":
    # 数据库设置
    DATABASES = DATABASES_TEST
elif RUN_MODE == "PRODUCT":
    # 数据库设置
    DATABASES = DATABASES_PRODUCT

ALLOWED_HOSTS = ['*']

# ==============================================================================
# Middleware and apps
# ==============================================================================
MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'account.middlewares.LoginMiddleware',
    'common.middlewares.CheckXssMiddleware',
)
MIDDLEWARE_CLASSES += MIDDLEWARE_CLASSES_CUSTOM

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    # OTHER 3rd Party App
    'account',
    'bkoauth',
)
INSTALLED_APPS += INSTALLED_APPS_CUSTOM


# ==============================================================================
# Django 项目配置
# ==============================================================================
TIME_ZONE = 'Asia/Shanghai'
LANGUAGE_CODE = 'zh-CN'
SITE_ID = 1
USE_I18N = True
USE_L10N = True

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR, PROJECT_MODULE_NAME = os.path.split(PROJECT_ROOT)
PYTHON_BIN = os.path.dirname(sys.executable)
# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(PROJECT_DIR, 'media/')
STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, 'static'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)
ROOT_URLCONF = 'urls'

#==============================================================================
# file upload handlers
#==============================================================================
FILE_UPLOAD_HANDLERS = (
    "django.core.files.uploadhandler.MemoryFileUploadHandler",
    "django.core.files.uploadhandler.TemporaryFileUploadHandler",
)

# ==============================================================================
# Templates
# ==============================================================================
TEMPLATE_CONTEXT_PROCESSORS = (
    # the context to the templates
    'django.contrib.auth.context_processors.auth',
    'django.template.context_processors.request',
    'django.template.context_processors.csrf',
    'common.context_processors.mysetting',      # 自定义模版context，可以在页面中使用STATIC_URL等变量
    'django.template.context_processors.i18n',
)
# django template dir
TEMPLATE_DIRS = (
    # 绝对路径，比如"/home/html/django_templates" or "C:/www/django/templates".
    os.path.join(PROJECT_ROOT, 'templates'),
)
# mako template dir
MAKO_TEMPLATE_DIR = os.path.join(PROJECT_ROOT, 'templates')
MAKO_TEMPLATE_MODULE_DIR = os.path.join(PROJECT_DIR, 'templates_module', APP_CODE)
if RUN_MODE is not 'DEVELOP':
    MAKO_TEMPLATE_MODULE_DIR = os.path.join(PROJECT_ROOT, 'templates_module', APP_CODE)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': list(TEMPLATE_DIRS),
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': list(TEMPLATE_CONTEXT_PROCESSORS),
        },
    },
]
# ==============================================================================
# session and cache
# ==============================================================================
SESSION_EXPIRE_AT_BROWSER_CLOSE = True       # 默认为false,为true时SESSION_COOKIE_AGE无效
SESSION_COOKIE_AGE = 60 * 60 * 24            # 单位--秒   60 * 60 * 24
SESSION_COOKIE_PATH = SITE_URL               # NOTE 不要改动，否则，可能会改成和其他app的一样，这样会影响登录
SESSION_ENGINE = 'django.contrib.sessions.backends.db'

# ===============================================================================
# Authentication
# ===============================================================================
AUTH_USER_MODEL = 'account.BkUser'
AUTHENTICATION_BACKENDS = ('account.backends.TicketBackend',)

# ===============================================================================
# FIXTURES (初始数据)
# ===============================================================================
# 包含initial_data.json的所有目录列表
# 如果有初始数据的需要, 请在initial_data.json中根据按格式加入
# 测试环境：t_fixtures/intial_data.json,正式环境：o_fixtures/intial_data.json
if RUN_MODE == 'PRODUCT':
    FIXTURE_FILE = os.path.join(PROJECT_DIR, PROJECT_MODULE_NAME, 'fixtures/o_fixtures/initial_data.json')
else:
    FIXTURE_FILE = os.path.join(PROJECT_DIR, PROJECT_MODULE_NAME, 'fixtures/t_fixtures/initial_data.json')

# ===============================================================================
# CELERY 配置
# ===============================================================================
if IS_USE_CELERY:
    try:
        import djcelery
        INSTALLED_APPS += (
            'djcelery',            # djcelery
        )
        djcelery.setup_loader()
        CELERY_ENABLE_UTC = False
        CELERYBEAT_SCHEDULER = "djcelery.schedulers.DatabaseScheduler"
        if "celery" in sys.argv:
            DEBUG = False
        # 本地开发时， BROKER_URL 可以在“config/settings_develop.py”中修改
        if RUN_MODE is not 'DEVELOP':
            BROKER_URL = BROKER_URL_ENV     # 从环境相关的配置文件中取得BROKER_URL
        if RUN_MODE == 'DEVELOP':
            from celery.signals import worker_process_init
            @worker_process_init.connect
            def configure_workers(*args, **kwargs):
                import django
                django.setup()
    except:
        pass

# ==============================================================================
# logging
# ==============================================================================
# SERVER_EMAIL = '**@tencent.com'
ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)
MANAGERS = ADMINS
LOGGING_DIR = os.path.join(PROJECT_DIR, 'logs', APP_CODE)

if RUN_MODE == "DEVELOP":
    LOG_LEVEL = LOG_LEVEL_DEVELOP
    LOG_CLASS = 'logging.handlers.RotatingFileHandler'
elif RUN_MODE == "TEST":
    LOGGING_DIR = LOGGING_DIR_ENV   # 使用环境相关的LOGGING_DIR
    LOG_CLASS = 'logging.handlers.RotatingFileHandler'
    LOG_LEVEL = LOG_LEVEL_TEST
elif RUN_MODE == "PRODUCT":
    LOGGING_DIR = LOGGING_DIR_ENV   # 使用环境相关的LOGGING_DIR
    LOG_LEVEL = LOG_LEVEL_PRODUCT
    LOG_CLASS = 'logging.handlers.RotatingFileHandler'


# 自动建立这个目录
if not os.path.exists(LOGGING_DIR):
    try:
        os.makedirs(LOGGING_DIR)
    except:
        pass

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s [%(asctime)s] %(pathname)s %(lineno)d %(funcName)s %(process)d %(thread)d \n \t %(message)s \n',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
        'simple': {
            'format': '%(levelname)s %(message)s \n'
        },
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'django.utils.log.NullHandler',
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'root': {
            'class': LOG_CLASS,
            'formatter': 'verbose',
            'filename': os.path.join(LOGGING_DIR, '%s.log' % APP_CODE),
            'maxBytes': 1024 * 1024 * 10,
            'backupCount': 5
        },
        'component': {
            'class': LOG_CLASS,
            'formatter': 'verbose',
            'filename': os.path.join(LOGGING_DIR, 'component.log'),
            'maxBytes': 1024 * 1024 * 10,
            'backupCount': 5
        },
        'wb_mysql': {
            'class': LOG_CLASS,
            'formatter': 'verbose',
            'filename': os.path.join(LOGGING_DIR, 'wb_mysql.log'),
            'maxBytes': 1024*1024*4,
            'backupCount': 5
        },
    },
    'loggers': {
        'django': {
            'handlers': ['null'],
            'level': 'INFO',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': True,
        },
        # the root logger ,用于整个project的logger
        'root': {
            'handlers': ['root'],
            'level': LOG_LEVEL,
            'propagate': True,
        },
        # 组件调用日志
        'component': {
            'handlers': ['component'],
            'level': 'WARN',
            'propagate': True,
        },
        # other loggers...
        'django.db.backends': {
            'handlers': ['wb_mysql'],
            'level': 'DEBUG',
            'propagate': True,
        },
    }
}
