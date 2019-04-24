# -*- coding: utf-8 -*-
from .conf import oauth_client

from ...client import ComponentClient
from ... import conf

import logging
logger = logging.getLogger('component')

__all__ = [
    'get_client_by_request',
    'get_client_by_user',
]


def get_client_by_request(request, **kwargs):
    """根据当前请求返回一个client

    :param request: 一个django request实例
    :returns: 一个初始化好的ComponentClint对象
    """
    # 兼容新版本框架：
    # @hydrapan: qcloud版的user表有变化， 我看组件用到了，明天我跟你说下
    #
    # 为了统一， 我给改回auth.user了， 现在用的是account.model.user吧
    # 能不能兼容一下， 判断如果没有account.model.user就用auth.user
    # 2017-2-23，老的User表取消，用了oauth后，User表的token会失效

    openid = ''
    access_token = ''
    if request.user.is_authenticated():
        openid = request.user.username

        # 新的access_token
        try:
            access_token_obj = oauth_client.get_access_token(request)
            access_token = access_token_obj.access_token
        except Exception:
            logger.exception(u"bkoauth根据openid（%s）获取access_token失败" % request.user.username)

    common_args = {
        'access_token': access_token,
        'openid': openid,
        'openkey': request.COOKIES.get('openkey', ''),
    }
    common_args.update(kwargs)
    return ComponentClient(conf.APP_CODE, conf.SECRET_KEY, common_args=common_args)


def get_client_by_user(user, **kwargs):
    """根据user实例返回一个client

    :param user: User实例或者openid
    :returns: 一个初始化好的ComponentClint对象
    """
    # 2017-2-23，老的User表取消，用了oauth后，User表的token会失效

    access_token = ''
    try:
        try:
            from django.contrib.auth import get_user_model
            User = get_user_model()  # noqa
        except:
            try:
                from account.models import User
            except:
                from django.contrib.auth.models import User

        if not isinstance(user, User):
            user = User.objects.get(username=user)
        try:
            # 新的access_token，会自动根据refresh_token刷新
            access_token_obj = oauth_client.get_access_token_by_user(user.username)
            access_token = access_token_obj.access_token
        except Exception as error:
            logger.warning(u"get_client_by_user: %s，兼容使用老的auth_token，请重新登录解决" % error)
            # 没有access_token兼容老的auth_token
            access_token = user.auth_token
    except Exception:
        logger.exception(u"根据user（%s）获取access_token失败" % user)

    common_args = {'access_token': access_token}
    common_args.update(kwargs)
    return ComponentClient(conf.APP_CODE, conf.SECRET_KEY, common_args=common_args)
