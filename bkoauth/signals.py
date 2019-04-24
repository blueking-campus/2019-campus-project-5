# -*- coding: utf-8 -*-
import logging

from django.contrib.auth.signals import user_logged_in

from .client import oauth_client

LOG = logging.getLogger('component')


def update_user_access_token(sender, request, user, *args, **kwargs):
    """自动刷新access_token
    """
    try:
        access_token = oauth_client.get_access_token(request)
        LOG.info('user logged in get access_token success: %s' % access_token)
    except Exception as error:
        LOG.exception('user logged in get access_token failed: %s' % error)

user_logged_in.connect(update_user_access_token)
