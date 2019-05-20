# -*- coding: utf-8 -*-
from django.conf.urls import (
    patterns,
    url
)

urlpatterns = patterns(
    'home_application.views',
    # 首页--your index

    url(r'^$', 'home', name='home'),    # 首页

    url(r'^manage/awards/add/$', 'manage_add_award', name='manage_add_award'),             # 添加奖项页面
    url(r'^manage/awards/clone/$', 'manage_clone_award', name='manage_clone_award'),       # 克隆奖项页面
    url(r'^manage/awards/change/$', 'manage_change_award', name='manage_change_award'),    # 修改奖项页面
    url(r'^manage/awards/show/$', 'manage_show_award', name='manage_show_award'),          # 展示奖项页面
    url(r'^manage/awards/$', 'manage_awards', name='manage_awards'),                       # 奖项管理页面
    url(r'^manage/organizations/$', 'manage_organizations', name='manage_organizations'),  # 组织管理页面

    url(r'^personal/apply/$', 'personal_apply', name='personal_apply'),                         # 我的申报页面
    url(r'^personal/change_apply/$', 'personal_change_apply', name='personal_change_apply'),    # 修改奖项申请页面
    url(r'^personal/show_apply/$', 'personal_show_apply', name='personal_show_apply'),          # 查看奖项申请页面
    url(r'^personal/reapply/$', 'personal_reapply', name='personal_reapply'),                   # 重新申请页面
    url(r'^personal/review/$', 'personal_review', name='personal_review'),                      # 我的审核页面
    url(r'^personal/give_award/$', 'give_award', name='give_award'),                   # 评奖页面
    url(r'^personal/pass_award/$', 'pass_award', name='pass_award'),                   # 通过
    url(r'^personal/reject_award/$', 'reject_award', name='reject_award'),                   # 驳回


    url(r'^application/apply/$', 'application_apply', name='application_apply'),    # 奖项申请页面

    url(r'^login_qq/$', 'login_qq', name='login_qq'),                       # 手动登记QQ页面

    url(r'^api/all_awards/$', 'api_all_awards', name='api_awards'),                      # 查询所有awards
    url(r'^api/all_organizations/$', 'api_all_organizations', name='api_organizations'), # 查询所有组织
    url(r'^api/add_award/$', 'api_add_award', name='api_add_award'),                     # 增加award
    url(r'^api/change_award/$', 'api_change_award', name='api_change_award'),            # 修改award
    url(r'^api/delete_award/$', 'api_delete_award', name='api_delete_award'),            # 删除award
    url(r'^api/delete_organizations/$', 'api_delete_organizations', name='api_delete_organizations'),  # 删除organizations

    url(r'^api/my_apply/$', 'api_my_apply', name='api_my_apply'),               # 查询所有我的申请
    url(r'^api/my_review/$', 'api_my_review', name='api_my_review'),               # 查询所有我的审核
    url(r'^api/change_apply/$', 'api_change_apply', name='api_change_apply'),   # 查询所有我的申请
    url(r'^api/reapply/$', 'api_reapply', name='api_reapply'),                  # 重新申请
    url(r'^api/apply/$', 'api_apply', name='api_apply'),                        # 奖项申报



    url(r'^api/login_qq/$', 'api_login_qq', name='api_login_qq'),       # 登记qq

    url(r'^api/add_organizations/$', 'api_add_organizations', name='api_add_organizations'),  #增加组织
    url(r'^api/delete_organizations/$', 'api_delete_organizations', name='api_delete_organizations'),
)
