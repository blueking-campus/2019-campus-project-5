# -*- coding: utf-8 -*-
"""
account的一些公用方法
"""
import urlparse

from django.conf import settings

from common.log import logger


def http_referer(request):
    """
    获取 HTTP_REFERER 头
    """
    if 'HTTP_REFERER' in request.META:
        http_referer = urlparse.urlparse(request.META['HTTP_REFERER'])[2]
    else:
        from account.factories import AccountFactory
        account = AccountFactory.getAccountObj()
        http_referer = account._config.LOGIN_REDIRECT_URL
    return http_referer


def is_url_in_domain(url):
    """
    判断url是否在当前域名下
    """
    try:
        url_pares = urlparse.urlparse(url)
        netloc = url_pares.netloc
        netloc = netloc.split(':')[0]
        # django 的next为 /或者 /?app=appcode
        if netloc == '' or netloc == settings.APP_HOST_DOMAIN:
            return True
    except Exception, e:
        logger.error(u"获取url的域名出错:%s, url:%s" % (e, url))
    return False
