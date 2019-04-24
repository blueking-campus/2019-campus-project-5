# -*- coding: utf-8 -*-
import datetime

from django.db import models

from .django_conf import EXPIRES_SECONDS, APP_CODE


class AccessToken(models.Model):
    access_token = models.CharField(u"Access Token", max_length=255, unique=True)
    expires = models.DateTimeField(u"Access Token过期时间")
    refresh_token = models.CharField(u"Refresh Token", max_length=255, null=True, blank=True)
    scope = models.TextField(u"权限范围", null=True, blank=True)
    env_name = models.CharField(u"部署环境", max_length=255, db_index=True)
    user_id = models.CharField('user_id', max_length=64, null=True, blank=True, db_index=True)
    created_at = models.DateTimeField(u"创建时间", auto_now_add=True)
    extra = models.TextField(u"其他", null=True, blank=True)

    class Meta:
        app_label = 'bkoauth'
        db_table = 'bkoauth_access_token'
        verbose_name = 'AccessToken'
        verbose_name_plural = 'AccessToken'

    def __unicode__(self):
        if self.user_id:
            return '<user(%s), access_token(%s)>' % (self.user_id, self.access_token)
        else:
            # APP级别access_token
            return '<app(%s), access_token(%s)>' % (APP_CODE, self.access_token)

    @property
    def expires_soon(self):
        """判断是否即将过期
        """
        now = datetime.datetime.now()
        return self.expires - now < datetime.timedelta(seconds=EXPIRES_SECONDS)
