# -*- coding: utf-8 -*-
"""BK user admin."""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _

from account.models import BkUser
from account.forms import BkUserChangeForm, BkUserCreationForm


class BkUserAdmin(UserAdmin):
    """
    The forms to add and change user instances.

    The fields to be used in displaying the User model.
    These override the definitions on the base UserAdmin
    """

    fieldsets = (
        (None, {'fields': ('username', 'password', 'auth_token', 'expires_time')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    form = BkUserChangeForm
    add_form = BkUserCreationForm


admin.site.register(BkUser, BkUserAdmin)
