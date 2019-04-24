# -*- coding: utf-8 -*-

"""
装饰器
1.权限pad装饰器，permission_required(已经写好装饰器，可自行定义验证逻辑)
"""
from django.http import HttpResponseForbidden
from django.utils.decorators import available_attrs
try:
    from functools import wraps
except ImportError:
    from django.utils.functional import wraps  # Python 2.4 fallback.


# ===============================================================================
# 转义装饰器
# ===============================================================================
def escape_exempt(view_func):
    """
    转义豁免，被此装饰器修饰的action可以不进行中间件escape
    """
    def wrapped_view(*args, **kwargs):
        return view_func(*args, **kwargs)
    wrapped_view.escape_exempt = True
    return wraps(view_func, assigned=available_attrs(view_func))(wrapped_view)


def escape_script(view_func):
    """
    被此装饰器修饰的action会对GET与POST参数进行javascript escape
    """
    def wrapped_view(*args, **kwargs):
        return view_func(*args, **kwargs)
    wrapped_view.escape_script = True
    return wraps(view_func, assigned=available_attrs(view_func))(wrapped_view)


def escape_url(view_func):
    """
    被此装饰器修饰的action会对GET与POST参数进行url escape
    """
    def wrapped_view(*args, **kwargs):
        return view_func(*args, **kwargs)
    wrapped_view.escape_url = True
    return wraps(view_func, assigned=available_attrs(view_func))(wrapped_view)


def escape_exempt_param(*param_list, **param_list_dict):
    """
    此装饰器用来豁免某个view函数的某个参数
    @param param_list: 参数列表
    @return:
    """
    def _escape_exempt_param(view_func):
        def wrapped_view(*args, **kwargs):
            return view_func(*args, **kwargs)
        if param_list_dict.get('param_list'):
            wrapped_view.escape_exempt_param = param_list_dict['param_list']
        else:
            wrapped_view.escape_exempt_param = list(param_list)
        return wraps(view_func, assigned=available_attrs(view_func))(wrapped_view)
    return _escape_exempt_param


# ==============================================================================
# 权限判断装饰器
# ==============================================================================
def permission_required(app_code):
    """
    Decorator for views that checks whether a user has a particular permission
    to access the app_code, redirecting to the 403 page if necessary.
    Unused.
    """
    def decorator(view_func):
        @wraps(view_func, assigned=available_attrs(view_func))
        def _wrapped_view(request, *args, **kwargs):
            # TODO 调用判断权限的方法
            # if 1 == 1:
            #     return view_func(request, *args, **kwargs)
            # 无权限直接返回禁止页面
            return HttpResponseForbidden()
        return _wrapped_view
    return decorator
