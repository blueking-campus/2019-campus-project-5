# -*- coding: utf-8 -*-
from django.conf.urls import (
    patterns,
    url
)

urlpatterns = patterns(
    'home_application.views',
    # 首页--your index

    url(r'^$', 'home', name='home'),    # 首页

    url(r'^manage/awards/add/$', 'add_award', name='manage_add_award'),             # 添加奖项页面
    url(r'^manage/awards/clone/$', 'clone_award', name='manage_clone_award'),       # 克隆奖项页面
    url(r'^manage/awards/change/$', 'change_award', name='manage_change_award'),    # 修改奖项页面
    url(r'^manage/awards/show/$', 'show_award', name='manage_show_award'),          # 展示奖项页面
    url(r'^manage/awards/$', 'awards', name='manage_awards'),                       # 奖项管理页面
    url(r'^manage/organizations/$', 'organizations', name='manage_organizations'),  # 组织管理页面
    url(r'^api/delete_organizations/$', 'api_delete_organizations', name='api_delete_organizations'),   # 删除organizations

    url(r'^personal/apply/$', 'apply', name='personal_apply'),      # 我的申报页面
    url(r'^personal/review/$', 'review', name='personal_review'),   # 我的审核页面
    url(r'^personal/review/awards_review/$', 'awards_review'),      # 奖项审批页面，通过按钮进入


    url(r'^login_qq/$', 'login_qq', name='login_qq'),               # 手动登记QQ页面

    url(r'^api/all_awards/$', 'api_all_awards', name='api_awards'),             # 查询所有awards
    url(r'^api/all_organizations/$', 'api_all_organizations', name='api_organizations'),             # 查询所有awards
    url(r'^api/add_award/$', 'api_add_award', name='api_add_award'),            # 增加award
    url(r'^api/change_award/$', 'api_change_award', name='api_change_award'),   # 修改award
    url(r'^api/delete_award/$', 'api_delete_award', name='api_delete_award'),   # 删除award
    url(r'^api/login_qq/$', 'api_login_qq', name='api_login_qq'),               # 登记qq
)
