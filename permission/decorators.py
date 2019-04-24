# -*- coding: utf-8 -*-
"""
BlueKing Permission Center
装饰器用法:

使用说明:
func_code请填写功能代码

示例如下：
from permission.decorators import bk_check_auth

@bk_check_auth('bmddf')
def index(request):
    pass

"""
import json

from django.utils.decorators import available_attrs
try:
    from functools import wraps
except ImportError:
    from django.utils.functional import wraps  # Python 2.4 fallback.

from permission.permissions import Permission, _response_for_failure


def bk_check_auth(func_code):
    """
    统一权限管理装饰器,
    function接收单个code
    返回信息0：成功
            1: 未授权 直接跳转返回给的链接
            2: 未授权，返回码为407和错误信息
    """
    def decorator(view_func):
        @wraps(view_func, assigned=available_attrs(view_func))
        def _wrapped_view(request, *args, **kwargs):
            biz_id = [-1]
            _permission = Permission(request, func_code, biz_id)
            _result, message = _permission.check_auth()
            if _result == 0:
                # 成功
                return view_func(request, *args, **kwargs)
            else:
                info = {'function': func_code}
                info = json.dumps(info)
                return _response_for_failure(request, _result, message, request.is_ajax(), info)
        return _wrapped_view
    return decorator
