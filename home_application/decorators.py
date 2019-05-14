# -*- coding: utf-8 -*-
from functools import wraps

from django.http import HttpResponse
from django.utils.decorators import available_attrs
from common.mymako import render_mako_context

from home_application.utils import is_int
from home_application.utils import is_vaild_datetime


def require_superuser(func):
    """修饰器-要求管理员"""
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_superuser:
            return func(request, *args, **kwargs)
        else:
            return render_mako_context(request, '403.html')
    return wrapper


def require_int_GET(func, name):

    @wraps(func, name)
    def wrapper(request, *args, **kwargs):
        data = request.GET.get(name)
        if is_int(data) or (data is None):
            return func(request, *args, **kwargs)
        else:
            return HttpResponse(name + '需要为整数，或者不上传该参数。', status=400)
    return wrapper

def require_int_GET(name):
    """
    传入整数或者不传入
    name: 验证的变量名
    """
    def decorator(func):
        @wraps(func, assigned=available_attrs(func))
        def inner(request, *args, **kwargs):
            data = request.GET.get(name)
            if is_int(data):
                return func(request, *args, **kwargs)
            else:
                return HttpResponse(name + '需要为整数', status=400)
        return inner
    return decorator

def require_datetime_GET(name):
    """
    传入整数或者不传入
    name: 验证的变量名
    """
    def decorator(func):
        @wraps(func, assigned=available_attrs(func))
        def inner(request, *args, **kwargs):
            data = request.GET.get(name)
            if (not is_vaild_datetime(data)) and data:
                # datetime不为空且不是datetime格式
                return HttpResponse('日期格式需要为：%Y-%m-%d %H:%M:%S，或者不传入该参数',status=400)
            return func(request, *args, **kwargs)
        return inner
    return decorator
