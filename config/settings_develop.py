# -*- coding: utf-8 -*-
'''
@summary: 全局常量设置
用于本地开发环境
'''
try:
    from local_settings import LOCAL_APP_CODE, LOCAL_SECRET_KEY,LOCAL_DATABASE
except ImportError:
    LOCAL_APP_CODE = ''
    LOCAL_SECRET_KEY = ''
    LOCAL_DATABASE = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',  # 我们默认用mysql
            'NAME': LOCAL_APP_CODE,  # 数据库名 (默认与APP_CODE相同)
            'USER': '',  # 你的数据库user
            'PASSWORD': '',  # 你的数据库password
            'HOST': '127.0.0.1',  # 开发的时候，使用localhost
            'PORT': '3306',  # 默认3306
        },
    }
# ===============================================================================
# APP 基本信息
# ===============================================================================
# TOCHANGE 在蓝鲸平台上注册的应用的编码
APP_CODE = LOCAL_APP_CODE
# APP 密钥
SECRET_KEY = LOCAL_SECRET_KEY
# ===============================================================================
# 数据库设置, 本地开发数据库设置
# ===============================================================================
DATABASES = LOCAL_DATABASE

# ===============================================================================
# 本地访问路径设置
# ===============================================================================
# APP访问路径
# 本地开发也采用的QQ登录，本地请 使用 appdev.o.qcloud.com 域名访问
# 在hosts中配置：127.0.0.1 appdev.o.qcloud.com
# 本地开发工程若不是用8000端口启动，需要将端口更改为工程启动的端口
S_URL = 'http://appdev.o.qcloud.com:8000'

# ===============================================================================
# CELERY 配置   本地开发的 celery 的消息队列（RabbitMQ）配置
# ===============================================================================
BROKER_URL = 'amqp://guest:guest@127.0.0.1:5672/'

# ===============================================================================
# 蓝鲸内部系统配置
# ===============================================================================
# 蓝鲸平台的地址
BK_URL = 'http://o.qcloud.com/console'
# 静态资源地址：
# REMOTE_STATIC_URL = '%s/static_api/' % BK_URL

# ===============================================================================
# 去除没有必要的警告
# ===============================================================================
SILENCED_SYSTEM_CHECKS = ['1_8.W001', 'fields.W161', 'fields.W122']

# 去除本地开发时 requests包 使用https 出现ssl的部分警告
try:
    import requests
    from requests.packages.urllib3.exceptions import (
        InsecureRequestWarning, InsecurePlatformWarning, SNIMissingWarning)
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    requests.packages.urllib3.disable_warnings(InsecurePlatformWarning)
    requests.packages.urllib3.disable_warnings(SNIMissingWarning)
except:
    pass
