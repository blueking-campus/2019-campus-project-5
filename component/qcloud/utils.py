# -*- coding: utf-8 -*-
import os
import re
import json
import base64
import hmac
import hashlib


def get_current_environ():
    """获取当前组件SDK所工作的环境，如果环境变量中有设置，直接使用环境变量值
    否则通过sites目录下查找。
    """
    if os.environ.get('BK_SDK_ENVIRON'):
        return os.environ['BK_SDK_ENVIRON']

    current_dir = os.path.dirname(os.path.abspath(__file__))
    sites_dir = os.path.join(current_dir, 'sites')
    sites = [d for d in os.listdir(sites_dir)
             if os.path.isdir(os.path.join(sites_dir, d)) and not re.search(r'^\.', d)]
    if not sites:
        raise Exception('Unable to initialize package, no available site found.')
    return sites[0]


def get_signature(method, path, app_secret, params=None, data=None):
    """获取Signature
    """
    kwargs = {}
    if params:
        kwargs.update(params)
    if data:
        data = json.dumps(data) if isinstance(data, dict) else data
        kwargs['data'] = data
    kwargs = '&'.join([
        '%s=%s' % (k, v)
        for k, v in sorted(kwargs.iteritems(), key=lambda x: x[0])
    ])
    orignal = '%s%s?%s' % (method, path, kwargs)
    signature = base64.b64encode(hmac.new(app_secret, orignal, hashlib.sha1).digest())
    return signature


class FancyDict(dict):
    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError, k:
            raise AttributeError(k)

    def __setattr__(self, key, value):
        self[key] = value

    def __delattr__(self, key):
        try:
            del self[key]
        except KeyError, k:
            raise AttributeError(k)


def get_bk_user_model():
    try:
        from django.contrib.auth import get_user_model
        User = get_user_model()
    except:
        try:
            from account.models import User
        except:
            from django.contrib.auth.models import User
    return User


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for
    else:
        ip = request.META['REMOTE_ADDR']
    return ip
