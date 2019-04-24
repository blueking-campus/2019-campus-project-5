# -*- coding: utf-8 -*-
"""组件API接口Client
"""
import requests
import json
import time
import random
import logging
import urlparse

from . import conf
from .utils import get_signature

# 关闭 urllib3 的 warning
try:
    requests.packages.urllib3.disable_warnings()
except:
    pass


logger = logging.getLogger('component')


class BaseComponentClient(object):
    """Base client class for component"""

    @classmethod
    def setup_components(self, components):
        self.available_collections = components

    def __init__(self, app_code=None, app_secret=None, common_args=None, use_test_env=False, timeout=None):
        """
        :param str app_code: App code to use
        :param str app_secret: App secret to use
        :param dict common_args: Args that will apply to every request
        :param bool use_test_env: whether use test version of components
        :param int timeout: timeout to request components
        """
        self.app_code = app_code or conf.APP_CODE
        self.app_secret = app_secret or conf.SECRET_KEY
        self.common_args = common_args or {}
        self._cached_collections = {}
        self.use_test_env = use_test_env
        self.timeout = timeout
        self._check_with_cc_test_env = False

    def set_use_test_env(self, use_test_env):
        """Change the value of use_test_env

        :param bool use_test_env: whether use test version of components
        """
        self.use_test_env = use_test_env

    def set_check_with_cc_test_env(self, check_with_cc_test_env):
        """do not use it in prod env"""
        self._check_with_cc_test_env = check_with_cc_test_env

    def set_timeout(self, timeout):
        self.timeout = timeout

    def merge_params_data_with_common_args(self, method, params, data):
        """每次请求时获取通用参数
        """
        if conf.CLIENT_ENABLE_SIGNATURE:
            common_args = dict(app_code=self.app_code, **self.common_args)
        else:
            common_args = dict(app_code=self.app_code, app_secret=self.app_secret, **self.common_args)
        if method == 'GET':
            _params = common_args.copy()
            _params.update(params or {})
            params = _params
        elif method == 'POST':
            _data = common_args.copy()
            _data.update(data or {})
            data = json.dumps(_data)
        return params, data

    def request(self, method, url, params=None, data=None, **kwargs):
        """Send request
        """
        # 判断是否应该访问测试环境组件
        headers = kwargs.pop('headers', {})
        if self.use_test_env:
            headers['x-use-test-env'] = '1'
        if self._check_with_cc_test_env:
            headers['x-check-with-cc-test-env'] = '1'

        params, data = self.merge_params_data_with_common_args(method, params, data)
        logger.debug('Calling %s %s with params=%s, data=%s', method, url, params, data)
        return requests.request(method, url, params=params, data=data, verify=False,
                                proxies={"http": None}, headers=headers, timeout=self.timeout, **kwargs)

    def __getattr__(self, key):
        if key not in self.available_collections:
            return getattr(super(BaseComponentClient, self), key)

        if key not in self._cached_collections:
            collection = self.available_collections[key]
            self._cached_collections[key] = collection(self)
        return self._cached_collections[key]


class ComponentClientWithSignature(BaseComponentClient):
    """Client class for component with signature"""

    def request(self, method, url, params=None, data=None, **kwargs):
        """Send request, will add "signature" parameter.
        """
        # 判断是否应该访问测试环境组件
        headers = kwargs.pop('headers', {})
        if self.use_test_env:
            headers['x-use-test-env'] = '1'
        if self._check_with_cc_test_env:
            headers['x-check-with-cc-test-env'] = '1'

        params, data = self.merge_params_data_with_common_args(method, params, data)
        if method == 'POST':
            params = {}

        url_path = urlparse.urlparse(url).path
        # Signature永远加在GET参数中
        params.update({
            'bk_timestamp': int(time.time()),
            'bk_nonce': random.randint(1, 2147483647),
        })
        params['signature'] = get_signature(method, url_path, self.app_secret, params=params, data=data)

        logger.debug('Calling %s %s with params=%s, data=%s', method, url, params, data)
        return requests.request(method, url, params=params, data=data, verify=False,
                                headers=headers, timeout=self.timeout, **kwargs)


# 根据是否开启signature来判断使用的Client版本
if conf.CLIENT_ENABLE_SIGNATURE:
    ComponentClient = ComponentClientWithSignature
else:
    ComponentClient = BaseComponentClient

ComponentClient.setup_components(conf.AVAILABLE_COLLECTIONS)


# Utils and Shortcuts
def get_component_client_by_user(user):
    """ **deprecated**

    根据给定的用户获取与该用户绑定的 `ComponentClient` 对象。

    :returns: 一个初始化好的ComponentClint对象
    """
    logger.warning('get_component_client_by_user deprecated, please use get_client_by_user instead')

    if not isinstance(user, basestring):
        user = user.username

    return ComponentClient(conf.APP_CODE, conf.SECRET_KEY, common_args={'uin': user})
