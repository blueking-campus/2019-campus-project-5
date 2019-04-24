# -*- coding: utf-8 -*-
'''
@summary: 用户自定义URLconf
'''

from django.conf.urls import patterns, include, url


# 用户自定义 urlconf
urlpatterns_custom = patterns(
    '',
    # 在home_application(根应用)里开始开发你的应用的主要功能
    # (此处home_application可以改成你想要的名字)
    url(r'^', include('home_application.urls')),
)
