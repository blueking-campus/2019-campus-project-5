# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect, Http404

from account.decorators import login_exempt
from account.factories import AccountFactory
from account.settings_account import SITE_URL


@login_exempt
def login(request):
    # 不接受POST请求
    if request.method != 'GET':
        raise Http404()

    account = AccountFactory.getAccountObj()
    return account.login(request)


@login_exempt
def logout(request):
    account = AccountFactory.getAccountObj()
    return account.logout(request)


@login_exempt
def check_failed(request):
    """
    权限验证错误页面
    """
    account = AccountFactory.getAccountObj()
    return account.check_failed(request)


@login_exempt
def login_page(request):
    """
    平台统一登录页面
    """
    account = AccountFactory.getAccountObj()
    return account.login_page(request)


@login_exempt
def login_success(request):
    """
    登录成功页面
    """
    account = AccountFactory.getAccountObj()
    return account.login_success(request)


@login_exempt
def get_login_state(request):
    """
    获取登录态
    """
    account = AccountFactory.getAccountObj()
    # 重定向到首页
    response = HttpResponseRedirect(SITE_URL)
    # 处理登录的cookie
    response = account.handel_response(request, response)
    return response
