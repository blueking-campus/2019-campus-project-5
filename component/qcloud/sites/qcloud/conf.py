# -*- coding: utf-8 -*-
"""Conf for component client"""
from bkoauth.client import OAuthClient

from ...django_conf import APP_CODE, SECRET_KEY, RUN_MODE


__all__ = [
    'APP_CODE',
    'SECRET_KEY',
    'RUN_MODE',
    'COMPONENT_SYSTEM_HOST',
    'CLIENT_ENABLE_SIGNATURE',
    'AVAILABLE_COLLECTIONS',
]

if RUN_MODE == "DEVELOP":
    COMPONENT_SYSTEM_HOST = 'https://api-t.o.qcloud.com/c/qcloud'
elif RUN_MODE == "TEST":
    COMPONENT_SYSTEM_HOST = 'https://api-t.o.qcloud.com/c/qcloud'
elif RUN_MODE == "PRODUCT":
    COMPONENT_SYSTEM_HOST = 'https://api.o.qcloud.com/c/qcloud'

CLIENT_ENABLE_SIGNATURE = True

# bkoauth配置项
OAUTH_API_URL = 'https://apigw.o.qcloud.com'
OAUTH_COOKIES_PARAMS = {'openid': 'openid', 'openkey': 'openkey'}
oauth_client = OAuthClient(OAUTH_API_URL, OAUTH_COOKIES_PARAMS)

# Available components
from .apis.oidb import CollectionsOIDB
from .apis.qcloud_cmsi import CollectionsQcloudCMSI

AVAILABLE_COLLECTIONS = {
    'oidb': CollectionsOIDB,
    'qcloud_cmsi': CollectionsQcloudCMSI,
}
