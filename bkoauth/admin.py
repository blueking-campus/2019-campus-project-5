# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import AccessToken


class AccessTokenAdmin(admin.ModelAdmin):
    list_display = ('access_token', 'refresh_token', 'expires', 'user_id')
    search_fields = ('user_id', )

admin.site.register(AccessToken, AccessTokenAdmin)
