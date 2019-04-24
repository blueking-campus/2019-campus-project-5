# -*- coding: utf-8 -*-
"""Django 工程中的变量
"""

# 判断这个模块是否跑在Django环境下，如果在Django环境下，默认从settings中读取
# 配置信息，否则使用默认配置
# 客户端可采用import后再修改的方式来改变配置
try:
    from django.conf import settings

    APP_CODE = settings.APP_CODE
    SECRET_KEY = settings.SECRET_KEY
    RUN_MODE = settings.RUN_MODE
except:
    APP_CODE = None
    SECRET_KEY = None
    RUN_MODE = 'DEVELOP'
