# -*- coding: utf-8 -*-
from django.contrib import admin

from home_application.models import User, Level, Organization, Award, Application


class UserAdmin(admin.ModelAdmin):
    # 需要显示的字段信息
    list_display = ('qq', 'username')


class OrganizationAdmin(admin.ModelAdmin):
    # 需要显示的字段信息
    list_display = ('name', 'reviewer', 'applicant', 'manager')


class AwardAdmin(admin.ModelAdmin):
    # 需要显示的字段信息
    list_display = ('name', 'level', 'organization', 'is_active')


class ApplicationAdmin(admin.ModelAdmin):
    # 需要显示的字段信息
    list_display = ('applicant', 'introduction', 'status')

    fieldsets = (
        (None, {
            'fields': ('user', 'award', 'applicant', 'introduction', 'status', 'is_deleted', 'key')
        }),
    )


# 注册时，在第二个参数写上 admin model
admin.site.register(User, UserAdmin)
admin.site.register(Level)
admin.site.register(Organization)
# admin.site.register(Award)
# admin.site.register(Application)

