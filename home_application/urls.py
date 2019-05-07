# -*- coding: utf-8 -*-
from django.conf.urls import patterns

urlpatterns = patterns(
    'home_application.views',
    # 首页--your index

    (r'^$', 'home'),                   #首页
    (r'^manage/awards/$', 'awards'),   #奖项管理页面
    (r'^manage/organizations/$', 'organizations'), #组织管理页面
    (r'^manage/$',  'awards'),         #系统管理首页
    (r'^personal/$', 'apply'),         #个人中心首页
    (r'^personal/apply/$', 'apply'),   #我的申报页面
    (r'^personal/review/$', 'review'), #我的审核页面
    (r'^personal/review/awards_review/$', 'awards_review'), #奖项审批页面，通过按钮进入
    (r'^manage/awards/clone/$', 'clone'), #奖项克隆与编辑页面，通过按钮进入
)
