# -*- coding: utf-8 -*-
from django.conf.urls import patterns

urlpatterns = patterns(
    'home_application.views',
    # 首页--your index
    (r'^$', 'home'),
    (r'^manage/awards/$', 'awards'),
    (r'^manage/organizations/$', 'organizations'),
    (r'^manage/$', 'manage'),
    (r'^personal/$', 'personal'),
)
