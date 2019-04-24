# -*- coding: utf-8 -*-
from ....base import ComponentAPI


class CollectionsQcloudCMSI(object):
    """Collections of Qcloud_CMSI APIS"""

    def __init__(self, client):
        self.client = client

        # Execute
        self.send_email = ComponentAPI(
            client=self.client, method='POST', path='/compapi/qcloud_cmsi/send_mail_for_external_user/',
            description=u'发送邮件'
        )
        self.send_sms = ComponentAPI(
            client=self.client, method='POST', path='/compapi/qcloud_cmsi/send_sms_for_external_user/',
            description=u'发送短信'
        )       


