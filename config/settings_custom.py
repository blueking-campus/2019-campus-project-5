# -*- coding: utf-8 -*-
"""
用户自定义全局常量设置
"""
import os

from config.settings_env import APP_CODE, APP_PWD, DB_HOST_DFT, DB_PORT_DFT
# ==============================================================================
# 中间件和应用
# ==============================================================================
# 自定义中间件
MIDDLEWARE_CLASSES_CUSTOM = (
)
# 自定义APP
INSTALLED_APPS_CUSTOM = (
    # add your app here...
    'home_application',
)

# ===============================================================================
# 静态资源
# ===============================================================================
# 静态资源文件(js,css等）在APP上线更新后, 由于浏览器有缓存, 可能会造成没更新的情况.
# 所以在引用静态资源的地方，都把这个加上，如：<script src="/a.js?v=${STATIC_VERSION}"></script>；
# 如果静态资源修改了以后，上线前改这个版本号即可
STATIC_VERSION = 2.0

# ===============================================================================
# CELERY 配置
# ===============================================================================
# APP是否使用celery
IS_USE_CELERY = False           # APP 中 使用 celery 时，将该字段设为 True
# TOCHANGE调用celery任务的文件路径, 即包含如下语句的文件： from celery import task
CELERY_IMPORTS = ()

# ===============================================================================
# 数据库设置 ，APP中使用外部数据库时可以在这里修改数据库设置
# ===============================================================================
DB_NAME = os.environ.get('BK_APP_CODE', APP_CODE)
DB_PWD = os.environ.get('BK_APP_PWD', APP_PWD)
# 数据库的配置信息
DB_HOST = os.environ.get('BK_DB_HOST', DB_HOST_DFT)
DB_PORT = os.environ.get('BK_DB_PORT', DB_PORT_DFT)
# 测试环境数据库设置
DATABASES_TEST = {
    # default 请不要做修改 ！！！！！！！！！！
    'default':
    {
        'ENGINE': 'django.db.backends.mysql',  # 我们默认用mysql
        'NAME': DB_NAME,                             # 数据库名(与APP_CODE相同)
        'USER': DB_NAME,                              # 你的数据库user(与APP_CODE相同)
        'PASSWORD': DB_PWD,                       # 你的数据库password
        'HOST': DB_HOST,                               # APP数据库主机
        'PORT': DB_PORT,                               # APP数据库端口
    },
}

# 正式环境数据库设置
DATABASES_PRODUCT = {
    # default 请不要做修改 ！！！！！！！！！！
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # 我们默认用mysql
        'NAME': DB_NAME,                             # 数据库名(默认与APP_CODE相同)
        'USER': DB_NAME,                              # 你的数据库user
        'PASSWORD': DB_PWD,                       # 你的数据库password
        'HOST': DB_HOST,                                # 不需要改动
        'PORT': DB_PORT,                                   # 不需要改动
    },
}

# ===============================================================================
# 日志级别
# ===============================================================================
# 本地开发环境日志级别
LOG_LEVEL_DEVELOP = 'DEBUG'
# 测试环境日志级别
LOG_LEVEL_TEST = 'INFO'
# 正式环境日志级别
LOG_LEVEL_PRODUCT = 'ERROR'

# ===============================================================================
# 统一权限管理功能开关
# ===============================================================================
ENABLE_BK_AUTH = True
