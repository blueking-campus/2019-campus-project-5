# -*- coding: utf-8 -*-
import datetime
import logging

from django.db.models import Q
from requests import exceptions as req_exceptions
import requests

from .django_conf import APP_CODE, SECRET_KEY, ENV_NAME, \
    OAUTH_COOKIES_PARAMS, OAUTH_PARAMS, OAUTH_API_URL, \
    IS_BKOAUTH_IN_INSTALLED_APPS
from .models import AccessToken
from .utils import transform_uin, get_client_ip

from .exceptions import TokenNotExist, TokenAPIError

LOG = logging.getLogger('component')

# 使用连接池
rpool = requests.Session()


class OAuthClient(object):
    def __init__(self, api_url, auth_cookies_params, **auth_params):
        self.app_code = APP_CODE
        self.secret_key = SECRET_KEY
        self.env_name = ENV_NAME

        self.api_url = api_url
        self.auth_cookies_params = auth_cookies_params
        self.auth_params = auth_params

        if not self.is_enabled:
            LOG.warning(u'应用的 bkoauth 配置不完整')

    @property
    def is_enabled(self):
        return IS_BKOAUTH_IN_INSTALLED_APPS and self.api_url and self.auth_cookies_params

    def _get_app_access_token_data(self):
        path = '/auth_api/token/'
        url = '%s%s' % (self.api_url, path)
        params = {'app_code': self.app_code,
                  'app_secret': self.secret_key,
                  'env_name': self.env_name,
                  'grant_type': 'client_credentials'}
        try:
            resp = rpool.get(url, params=params, timeout=10, verify=False)
            resp = resp.json()
        except req_exceptions.MissingSchema:
            raise TokenAPIError(
                '1')
        except Exception as error:
            LOG.exception(u"获取APP级别access_token异常: %s" % error)
            raise TokenAPIError(error.message)

        if not resp.get('result'):
            LOG.error(u"获取APP级别access_token错误: %s" % resp.get('message', ''))
            raise TokenAPIError(resp.get('message', ''))

        data = resp['data']
        return data

    def _get_auth_params(self, request):
        """获取用户认证参数
        """
        params = self.auth_params
        for k, v in self.auth_cookies_params.items():
            # 非UIN也会每次检查
            v = transform_uin(request.COOKIES.get(v) or request.session.get(v) or request.GET.get(v, ''))
            params[k] = v
        return params

    def _get_access_token_data(self, request):
        path = '/auth_api/token/'
        url = '%s%s' % (self.api_url, path)
        params = {'app_code': self.app_code,
                  'app_secret': self.secret_key,
                  'env_name': self.env_name,
                  'bk_client_ip': get_client_ip(request),
                  'grant_type': 'authorization_code'}
        params.update(self._get_auth_params(request))
        try:
            resp = rpool.get(url, params=params, timeout=10, verify=False)
            resp = resp.json()
        except req_exceptions.MissingSchema:
            raise TokenAPIError(
                '1')
        except Exception as error:
            LOG.exception(u"获取用户级别access_token异常: %s" % error)
            raise TokenAPIError(error.message)

        if not resp.get('result'):
            LOG.error(u'获取用户级别access_token错误: %s' % resp.get('message', ''))
            raise TokenAPIError(resp.get('message', ''))

        data = resp['data']
        return data

    def _get_refresh_token_data(self, refresh_token, env_name):
        path = '/auth_api/refresh_token/'
        url = '%s%s' % (self.api_url, path)
        params = {'grant_type': 'refresh_token',
                  'app_code': self.app_code,
                  'env_name': env_name,
                  'refresh_token': refresh_token}
        try:
            resp = rpool.get(url, params=params, timeout=10, verify=False)
            resp = resp.json()
        except req_exceptions.MissingSchema:
            raise TokenAPIError(
                '1')
        except Exception as error:
            LOG.exception(u"刷新access_token异常: %s" % error)
            raise TokenAPIError(error.message)
        if not resp.get('result'):
            LOG.error(u'刷新access_token错误: %s' % resp.get('message', ''))
            raise TokenAPIError(resp.get('message', ''))

        data = resp['data']
        return data

    def get_app_access_token(self):
        """获取APP基本access_token
        """
        access_token = AccessToken.objects.filter(env_name=ENV_NAME)
        access_token = access_token.filter(Q(user_id__isnull=True) | Q(user_id__exact=''))
        if not access_token:
            data = self._get_app_access_token_data()
            expires = datetime.datetime.now() + datetime.timedelta(seconds=data['expires_in'])
            token = AccessToken(access_token=data['access_token'],
                                refresh_token=data.get('refresh_token', ''),
                                scope=data.get('scope', ''),
                                expires=expires,
                                env_name=ENV_NAME,)
            token.save()
            return token
        token = access_token[0]
        # 自动续期
        if token.expires_soon:
            data = self._get_app_access_token_data()
            expires = datetime.datetime.now() + datetime.timedelta(seconds=data['expires_in'])
            token.access_token = data['access_token']
            token.refresh_token = data.get('refresh_token', '')
            token.scope = data.get('scope', '')
            token.expires = expires
            token.save()
        return token

    def get_access_token(self, request):
        """获取用户access_token
        params: request django request对象
        """
        access_token = AccessToken.objects.filter(env_name=ENV_NAME, user_id=request.user.username)
        if not access_token:
            data = self._get_access_token_data(request)
            expires = datetime.datetime.now() + datetime.timedelta(seconds=data['expires_in'])
            token = AccessToken(user_id=request.user.username,
                                access_token=data['access_token'],
                                refresh_token=data.get('refresh_token', ''),
                                scope=data.get('scope', ''),
                                expires=expires,
                                env_name=ENV_NAME)

            token.save()
            return token
        token = access_token[0]
        # 自动续期
        if token.expires_soon:
            data = self._get_access_token_data(request)
            expires = datetime.datetime.now() + datetime.timedelta(seconds=data['expires_in'])
            token.access_token = data['access_token']
            token.refresh_token = data.get('refresh_token', '')
            token.scope = data.get('scope', '')
            token.expires = expires
            token.save()
        return token

    def get_access_token_by_user(self, user_id):
        """通过用户ID获取access_token，适合后台任务场景
        """
        access_token = AccessToken.objects.filter(env_name=ENV_NAME, user_id=user_id)
        if not access_token:
            raise TokenNotExist(u"获取用户【%s】access_token失败，数据库中不存在记录" % user_id)
        token = access_token[0]
        # 自动续期
        if token.expires_soon:
            token = self.refresh_token(token)
        return token

    def refresh_token(self, token):
        """刷新access_token
        params: token AccessToken对象
        """
        if not token.refresh_token:
            raise TokenNotExist(u"【%s】没有refresh_token，不能刷新" % token)
        data = self._get_refresh_token_data(token.refresh_token, token.env_name)
        expires = datetime.datetime.now() + datetime.timedelta(seconds=data['expires_in'])
        token.access_token = data['access_token']
        token.refresh_token = data.get('refresh_token', '')
        token.scope = data.get('scope', '')
        token.expires = expires
        token.save()
        return token

oauth_client = OAuthClient(OAUTH_API_URL, OAUTH_COOKIES_PARAMS, **OAUTH_PARAMS)
