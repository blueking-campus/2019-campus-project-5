# -*- coding: utf-8 -*-
"""
Django migrations for bkoauth app

This package does not contain South migrations.  South migrations can be found
in the ``south_migrations`` package.
"""

SOUTH_ERROR_MESSAGE = u"""\n
# 您的Django低于1.8版本, 请在配置文件中添加如下配置:
SOUTH_MIGRATION_MODULES = {
    'bkoauth': 'bkoauth.south_migrations',
}
"""

# Ensure the user is not using Django 1.8 or below with South
try:
    from django.db import migrations  # noqa
except ImportError:
    from django.core.exceptions import ImproperlyConfigured
    raise ImproperlyConfigured(SOUTH_ERROR_MESSAGE)
