# -*- coding: utf-8 -*-
"""
请不要修改该文件
如果你需要对settings里的内容做修改，请在config\settings_custom.py 文件中 添加即可
"""
import os
from settings import RUN_MODE
from settings_develop import APP_CODE as APP_CODE_DEV, SECRET_KEY as SECRET_KEY_DEV


# 框架运行环境
RUN_VER = 'qcloud'
# ==============================================================================
# APP 基本信息
# ==============================================================================
# APP 编码， 本地开发时在 config\settings_develop.py 文件中配置
APP_CODE = os.environ.get("BK_APP_CODE", APP_CODE_DEV)
# APP 密码 (数据库密码，MQ密码)
APP_PWD = os.environ.get("BK_APP_PWD", "")
# Make this unique, and don't share it with anybody.
SECRET_KEY = os.environ.get("BK_SECRET_KEY", SECRET_KEY_DEV)

# APP本地静态资源目录
STATIC_URL = os.environ.get("BK_STATIC_URL", "/static/")
# APP的url前缀, 不要修改. 如 "/your_app_code/", 在页面中使用
SITE_URL = os.environ.get("BK_SITE_URL", "/")
# APP静态资源目录url
REMOTE_STATIC_URL = os.environ.get('BK_REMOTE_STATIC_URL', 'http://o.qcloud.com/static_api/')
# logging目录
LOGGING_DIR_ENV = os.environ.get('BK_LOGGING_DIR', os.path.join('/data/logs/apps/', APP_CODE))
# 平台 URL
BK_URL = os.environ.get("BK_URL", "http://o.qcloud.com/console")
# celery 消息队列设置
BROKER_URL_ENV = os.environ.get('BK_BROKER_URL', '')

# 统一权限管理API host
PERMISSION_API_URL = os.environ.get('BK_PERMISSION_API_URL', 'http://login.o.qcloud.com/')
PERMISSION_CONSOLE_URL = os.environ.get('BK_PERMISSION_CONSOLE_URL', 'http://bk.tencent.com/campus/')

# APP域名(暂时没有)
APP_HOST_DOMAIN = '%s.test.qcloudapps.com' % APP_CODE
# 为True限制用户访问，白名单用户才能访问
RESTEICT_USER_ACCESS = False

# DB配置
DB_HOST_DFT = os.environ.get('BK_DB_HOST', "")
DB_PORT_DFT = os.environ.get('BK_DB_PORT', '')

# 测试环境配置
if RUN_MODE == 'TEST':
    # APP域名(暂时没有)
    APP_HOST_DOMAIN = '%s.test.qcloudapps.com' % APP_CODE

    # CSRF的COOKIE域
    CSRF_COOKIE_DOMAIN = os.environ.get('BK_CSRF_COOKIE_DOMAIN', '%s.test.qcloudapps.com' % (APP_CODE))
    # APP访问路径
    S_URL = os.environ.get("BK_S_URL", 'http://%s.test.qcloudapps.com' % (APP_CODE))
# 正式环境配置
elif RUN_MODE == 'PRODUCT':
    # APP域名(暂时没有)
    APP_HOST_DOMAIN = '%s.qcloudapps.com' % (APP_CODE)

    # CSRF的COOKIE域
    CSRF_COOKIE_DOMAIN = os.environ.get('BK_CSRF_COOKIE_DOMAIN', '%s.qcloudapps.com' % (APP_CODE))
    # APP访问路径
    S_URL = os.environ.get("BK_S_URL", 'http://%s.qcloudapps.com' % (APP_CODE))
