# -*- coding: utf-8 -*-
"""
登录装饰器
"""
from django.utils.decorators import available_attrs
from django.contrib.auth import REDIRECT_FIELD_NAME

from account.factories import AccountFactory

try:
    from functools import wraps
except ImportError:
    from django.utils.functional import wraps  # Python 2.4 fallback.


# ===============================================================================
# 登录豁免，被此装饰器修饰的action可以不校验登录态
# ===============================================================================
def login_exempt(view_func):
    """
    登录豁免，被此装饰器修饰的action可以不校验登录态
    """
    def wrapped_view(*args, **kwargs):
        return view_func(*args, **kwargs)
    wrapped_view.login_exempt = True
    return wraps(view_func, assigned=available_attrs(view_func))(wrapped_view)


# ===============================================================================
# 以下提供login_required装饰器， 是为了兼容老版本的App， 在升级Account模块时， 不需要改动太多代码
# ===============================================================================
def user_passes_test(test_func, login_url=None, redirect_field_name=REDIRECT_FIELD_NAME):
    """
    Decorator for views that checks that the user passes the given test,
    redirecting to the log-in page if necessary. The test should be a callable
    that takes the user object and returns True if the user passes.
    """
    def decorator(view_func):
        @wraps(view_func, assigned=available_attrs(view_func))
        def _wrapped_view(request, *args, **kwargs):

            # 判断用户登录状态是否OK
            account = AccountFactory.getAccountObj()
            loginStatus = account.check_user_login_status(request)
            if loginStatus == 0:
                response = view_func(request, *args, **kwargs)
                # 统一处理 response, 包括 cookie、session 等
                response = account.handel_response(request, response)
                return response

            # 判断视图是不是自定义了login_url和redirect_field_name
            loginUrl = account.getConfig().LOGIN_URL
            redirectFieldName = REDIRECT_FIELD_NAME

            # 对于登录态不OK的用户， 引导重新登录 （首页的直接跳登录页， 非首页的跳登录态错误页）
            return account.redirectReLogin(request, loginUrl, redirectFieldName)

        return _wrapped_view
    return decorator


def login_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=None):
    """
    Decorator for views that checks that the user is logged in, redirecting
    to the log-in page if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated(),
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator
