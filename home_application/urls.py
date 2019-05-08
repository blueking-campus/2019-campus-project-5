# -*- coding: utf-8 -*-
from django.conf.urls import (
    patterns,
    url
)

urlpatterns = patterns(
    'home_application.views',
    # 首页--your index

    url(r'^$', 'home', name='home'),                   #首页

    url(r'^manage/awards/$', 'awards', name='manage_awards'),   #奖项管理页面
    url(r'^manage/organizations/$', 'organizations', name='manage_organizations'), #组织管理页面

    url(r'^personal/apply/$', 'apply', name='personal_apply'),   #我的申报页面
    url(r'^personal/review/$', 'review', name='personal_review'), #我的审核页面
    url(r'^personal/review/awards_review/$', 'awards_review'), #奖项审批页面，通过按钮进入
    url(r'^manage/awards/clone/$', 'clone'), #奖项克隆与编辑页面，通过按钮进入

    url(r'^login_qq/$', 'login_qq', name='login_qq'),  #

    url(r'^api/all_awards/$', 'api_all_awards', name='api_awards'), # 查询所有awards
    url(r'^api/login_qq/$', 'api_login_qq', name='api_login_qq'), # 查询所有awards
)
