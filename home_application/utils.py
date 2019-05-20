# -*- coding: utf-8 -*-
import json
import time
import datetime
import uuid

from django.core.urlresolvers import reverse
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
from local_settings import secret_id, secret_key, region, scheme, token, Bucket
# from home_application.urls_settings import urls


class UrlSetting(object):
    def __init__(self):
        # url配置
        self.urls = {
            'home': {
                'url': reverse('home'),
                'title': u'首页'
            },
            'manage': {
                'url': '#',
                'title': u'系统管理'
            },
            'manage_awards': {
                'url': reverse('manage_awards'),
                'title': u'奖项管理'
            },
            'manage_organizations': {
                'url': reverse('manage_organizations'),
                'title': u'组织管理'
            },
            'manage_add_award': {
                'url': reverse('manage_add_award'),
                'title': u'添加奖项'
            },
            'manage_show_award': {
                'url': reverse('manage_show_award'),
                'title': u'奖项详情'
            },
            'manage_change_award': {
                'url': reverse('manage_change_award'),
                'title': u'修改奖项'
            },
            'application_apply': {
                'url': '#',
                'title': u'奖项申报'
            },
            'personal': {
                'url': '#',
                'title': u'个人管理'
            },
            'personal_apply': {
                'url': reverse('personal_apply'),
                'title': u'我的申报'
            },
            'personal_change_apply': {
                'url': '#',
                'title': u'修改申报'
            },
            'personal_show_apply': {
                'url': '#',
                'title': u'展示申报'
            },
            'personal_reapply': {
                'url': '#',
                'title': u'重新申请'
            },
            'personal_review': {
                'url': reverse('personal_review'),
                'title': u'我的审核'
            },
        }


    def get_setting(self):
        """获取配置"""
        return self.urls




class DateJSONEncoder(json.JSONEncoder):
    """date-json编码"""

    def default(self, o):
        if isinstance(o, datetime.datetime):
            return o.strftime("%Y-%m-%d %H:%M:%S")
        if isinstance(o, datetime.date):
            return o.strftime("%Y-%m-%d")
        else:
            return json.JSONEncoder.default(self, o)


def generateUUID(prefx=''):
    """生成uuid的hex"""
    newUuidHex = uuid.uuid4().hex
    newUuid = prefx + newUuidHex
    return newUuid


def is_vaild_datetime(date):
    """
    判断是否是datetime格式字符串
    date: %Y-%m-%d %H:%M:%S
    """
    try:
        time.strptime(date, "%Y-%m-%d %H:%M:%S")
        return True
    except ValueError, err:
        print err
        return False
    except TypeError, err:
        print err
        return False


def is_int(num):
    """判断是否是int格式的字符串"""
    try:
        int(num)
        return True
    except ValueError, err:
        print err
        return False
    except TypeError, err:
        print err
        return False


def get_url_list(name_lsit):
    """
    获取url_list
    name_list's item: string:url_name or dirc:{'url_name': string, 'kwargs':dirc }
    """

    url_setting = UrlSetting()
    urls = url_setting.get_setting()
    url_list = []
    for name in name_lsit:
        if isinstance(name, dict):
            url = urls.get(name['url_name'])
            url['url'] = ''.join([url['url'][0:-1], '?'])
            for key, value in name['kwargs'].items():
                arg = '='.join([key, value, '&'])
                url['url'] = ''.join([url['url'], arg])
        else:
            url = urls.get(name)
        url_list.append(url)
    return url_list


def get_file(key):
    """上传文件到腾讯cos"""
    config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key, Token=token, Scheme=scheme)
    # 获取客户端对象
    client = CosS3Client(config)
    response = client.get_object(
        Bucket=Bucket,
        Key=key,
        ResponseContentType='text/html; charset=utf-8'
    )
    return response


def put_file(key, file):
    """从腾讯cos下载文件"""
    config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key, Token=token, Scheme=scheme)
    # 获取客户端对象
    client = CosS3Client(config)
    body = file
    response = client.put_object(
        Bucket=Bucket,
        Body=body,
        Key=key,
        EnableMD5=False
    )
    return response


def delete_file(key):
    """从腾讯cos删除文件"""
    config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key, Token=token, Scheme=scheme)
    # 获取客户端对象
    client = CosS3Client(config)
    client.delete_object(
        Bucket=Bucket,
        Key=key
    )
    return True
