# -*- coding: utf-8 -*-
from django.contrib.auth.backends import ModelBackend
from account.factories import AccountFactory


class TicketBackend(ModelBackend):
    """
    后台验证
    """
    def authenticate(self, ticket=None, request=None):
        account = AccountFactory.getAccountObj()
        status, user = account.check_backend_login_status(request)

        if not status or not user:
            return None

        return user
