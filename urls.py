# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
# admin.autodiscover()
from django.conf import settings

from config.urls_custom import urlpatterns_custom

urlpatterns = patterns(
    '',
    # django后台数据库管理
    url(r'^admin/', include(admin.site.urls)),
    # 用户账号--不要修改
    url(r'^accounts/', include('account.urls')),
)

# app自定义路径
urlpatterns += urlpatterns_custom

if settings.RUN_MODE == 'DEVELOP':
    urlpatterns += patterns(
        '',
        # media
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
    )
