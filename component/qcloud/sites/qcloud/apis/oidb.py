# -*- coding: utf-8 -*-
from ....base import ComponentAPI


class CollectionsOIDB(object):
    """Collections of OIDB APIS"""

    def __init__(self, client):
        self.client = client

        # Query
        self.get_openid_openkey = ComponentAPI(
            client=self.client, method='GET', path='/compapi/oidb/get_openid_openkey/',
            default_return_value=[],
            description=u'获取OpenID和OpenKey'
        )
        self.get_user_info = ComponentAPI(
            client=self.client, method='GET', path='/compapi/oidb/get_user_info/',
            description=u'根据openid获取用户基本信息'
        )
        self.verify_openid_openkey = ComponentAPI(
            client=self.client, method='GET', path='/compapi/oidb/verify_openid_openkey/',
            description=u'验证OpenID和OpenKey或AccessToken'
        )
        # AUTH
        self.get_auth_token = ComponentAPI(
            client=self.client, method='POST', path='/compapi/auth/get_auth_token/',
            description=u'根据给定的openid/openkey组合来生成auth_token'
        )
