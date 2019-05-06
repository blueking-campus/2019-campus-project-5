# -*- coding: utf-8 -*-
from functools import wraps

from django.http import HttpResponse


def require_superuser(func):
    """修饰器-要求管理员"""
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_superuser:
            return func(request, *args, **kwargs)
        else:
            return HttpResponse('superuser required!')
    return wrapper
