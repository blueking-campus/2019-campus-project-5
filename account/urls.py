# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url


urlpatterns = patterns(
    'account.views',
    # login
    url(r'^login/$', 'login', name='login'),
    # logout
    url(r'^logout/$', 'logout', name='logout'),
    # 引导登录页
    url(r'^login_page/$', 'login_page', name='login_page'),
    # 登录成功
    url(r'^login_success/$', 'login_success', name='login_success'),
    # 权限验证错误页面
    url(r'^check_failed/$', 'check_failed', name='check_failed'),
    # 获取 openid openkey
    url(r'^get_login_state/$', 'get_login_state', name='get_login_state'),
)
