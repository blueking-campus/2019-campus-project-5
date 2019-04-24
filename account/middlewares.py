# -*- coding: UTF-8 -*-
"""
登录中间件
用来取代登录装饰器
app接口默认都需要登录验证， 在无需验证登录态的action上面主动标明无需验证登录态的装饰器
"""
from django.contrib.auth import REDIRECT_FIELD_NAME

from account.factories import AccountFactory


class LoginMiddleware(object):
    """
    登录中间件
    用来取代登录装饰器
    默认在每个请求上验证登录态， 在无需验证登录态的action上面主动标明无需验证登录态的装饰器
    """

    def process_view(self, request, view, args, kwargs):
        """
        校验登录， 如果未登录由跳转登录页
        """
        # 判断豁免权
        if getattr(view, 'login_exempt', False):
            return None

        # 判断用户登录状态是否OK
        account = AccountFactory.getAccountObj()
        loginStatus = account.check_user_login_status(request)
        if loginStatus == 0:
            return None

        # 判断视图是不是自定义了login_url和redirect_field_name
        loginUrl = getattr(view, 'login_url', account.getConfig().LOGIN_URL)
        redirectFieldName = getattr(view, 'redirect_field_name', REDIRECT_FIELD_NAME)

        # 对于登录态不OK的用户， 引导重新登录 （首页的直接跳登录页， 非首页的跳登录态错误页）
        return account.redirectReLogin(request, loginUrl, redirectFieldName)

    def process_response(self, request, response):
        """
        统一处理response请求
        """
        account = AccountFactory.getAccountObj()
        # 统一处理 response, 包括 cookie、session 等
        response = account.handel_response(request, response)
        return response
