# -*- coding: utf-8 -*-
"""
登录相关的配置
"""
from account.settings_account import *

# 统一登录的plain模式， 适用于ajax等小窗登录
PLAIN_LOGIN_URL = 'http://login.o.qcloud.com/plain/?app_code=%s' % APP_CODE
# 跨域获取uin skey
CROSS_PREFIX = 'http://ptlogin2.tencent.com/ho_cross_domain?tourl='
# 统一登录的登录页
LOGIN_URL = 'http://login.o.qcloud.com/?app_code=%s' % APP_CODE  # 需要传入app_code和c_url

S_URL = settings.S_URL
