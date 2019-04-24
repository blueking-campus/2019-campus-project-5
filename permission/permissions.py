# -*- coding: utf-8 -*-
import base64
import hashlib
import hmac
import json
import random
import socket
import time
import urlparse
from urllib2 import urlopen
from urllib import urlencode, quote

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import redirect
from django.utils.decorators import available_attrs

from common.log import logger

try:
    from functools import wraps
except ImportError:
    from django.utils.functional import wraps  # Python 2.4 fallback.


__VERSION__ = '0.1'

# 统一权限配置开关
FUNCTION_CONTROL = 'ENABLE_BK_AUTH'
# request缓存常量名
PERMISSION_CACHE = 'BK_PERMISSION_CACHE'

# API链接
API_HOST = settings.PERMISSION_API_URL
CONSOLE_HOST = settings.PERMISSION_CONSOLE_URL
GET_PERMISSIONS_URL = '%spermission/get_permissions/' % API_HOST
CHECK_FAILED_URL = '%spermission_center/check_failed/' % CONSOLE_HOST
CHECK_FAILED_AJAX_URL = '%spermission_center/check_failed_ajax/' % CONSOLE_HOST


def signer(view_func):
    """
    urlopen签名装饰器
    """
    # 获取基础信息
    app_code = getattr(settings, 'APP_CODE', '')
    app_secret = getattr(settings, 'SECRET_KEY', '')

    @wraps(view_func, assigned=available_attrs(view_func))
    def _wrapped_view(url, data=None, timeout=socket._GLOBAL_DEFAULT_TIMEOUT, **kwargs):
        _request = urlparse.urlparse(url)
        query = dict(urlparse.parse_qsl(_request.query))
        query['Nonce'] = random.randint(100000, 999999)
        query['Timestamp'] = int(time.time())
        query['app_code'] = app_code
        if not data:
            method = 'GET'
            _query = '&'.join(['%s=%s' % (i, query[i]) for i in sorted(query)])
        else:
            method = 'POST'
            query['Data'] = data
            _query = '&'.join(['%s=%s' % (i, query[i]) for i in sorted(query)])
            query.pop('Data', None)

        # 签名
        raw_msg = '%s%s%s?%s' % (method, _request.netloc, _request.path, _query)
        Signature = base64.b64encode(hmac.new(app_secret, raw_msg, hashlib.sha1).digest())
        query['Signature'] = Signature
        query = urlencode(query)
        # 带上签名参数
        url = '%s://%s%s?%s' % (_request.scheme, _request.netloc, _request.path, query)
        return view_func(url, data, timeout=timeout, **kwargs)
    return _wrapped_view


signed_urlopen = signer(urlopen)


class Permission(object):
    """
    统一权限API请求类
    """
    def __init__(self, request, func_code=None, biz_id=[-1]):
        self.uin = request.user.username
        self.enable = getattr(settings, FUNCTION_CONTROL, False)
        self.app_code = getattr(settings, 'APP_CODE', '')

        self._request = request
        self._func_code = func_code
        self._biz_id = biz_id

        self._cache = {}

    def get_permission(self, timeout=2):
        params = {'uin': self.uin, 'app_code': self.app_code}
        params = urlencode(params)
        url = '%s?%s' % (GET_PERMISSIONS_URL, params)
        try:
            resp = signed_urlopen(url, timeout=timeout).read()
            result = json.loads(resp)
            self.permission = result.get('permission', [])
            self.role = result.get('permission_role', -1)
        except:
            self.permission = []
            self.role = -1

    def _init_cache(self):
        if not self._cache:
            if hasattr(self._request, PERMISSION_CACHE):
                self._cache = getattr(self._request, PERMISSION_CACHE)
            else:
                self.get_permission()
                self._cache['role'] = self.role
                _func_biz = {}
                for i in self.permission:
                    if i['function_code'] not in _func_biz:
                        _func_biz[i['function_code']] = set([i['biz_id']])
                    else:
                        _func_biz[i['function_code']].add(i['biz_id'])
                self._cache['func_biz'] = _func_biz
                # request缓存权限
                setattr(self._request, PERMISSION_CACHE, self._cache)
        return self._cache

    @property
    def func_biz(self):
        """
        功能业务对应关系
        """
        self._init_cache()
        return self._cache['func_biz']

    @property
    def is_superuser(self):
        """
        是否超级用户,
        permission_role == 2表示超级用户
        """
        self._init_cache()
        return self._cache['role'] == 2

    def check_auth(self):
        """
        权限检查
        """
        try:
            if not self.enable:
                return (0, u"权限管理功能开关关闭,返回成功")

            if self.is_superuser:
                return (0, u"用户是超级用户,返回成功")

            _biz = self.func_biz.get(self._func_code)
            if _biz and _biz.intersection(self._biz_id):
                return (0, u"权限检查成功")

            return (2, u"没有权限")
        except Exception as error:
            logger.error('permission check_auth error: %s' % error)
            return (2, u"请求异常")


def _response_for_failure(request, _result, message, is_ajax, info):
    """
    内部通用方法: 请求敏感权限出错时的处理(1和2)
    @param _result: 结果标志位
    @param message: 结果信息
    @param is_ajax: 是否是ajax请求
    """
    if _result == 1:
        # 登陆失败，需要重新登录,跳转至登录页
        if is_ajax:
            return HttpResponse(status=402)
        return redirect(message)
    elif _result == 2:
        # error(包括exception)
        return _redirect_402(request, info)


def _redirect_402(request, info):
    """
    转到402权限不足的提示页面
    """
    app_code = settings.APP_CODE
    run_mode = settings.RUN_MODE
    if request.is_ajax():
        url = CHECK_FAILED_AJAX_URL + '?app_code=%s&run_mode=%s&info=%s' % (app_code, run_mode, quote(info))
        resp = HttpResponse(status=402, content=url)
        return resp
    else:
        url = CHECK_FAILED_URL + '?app_code=%s&run_mode=%s&info=%s' % (app_code, run_mode, info)
        return redirect(url)
