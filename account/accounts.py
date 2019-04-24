# -*- coding: utf-8 -*-
"""
账号体系相关的基类Account
"""
import urllib
import urlparse

from django.contrib import auth
from django.contrib.auth import REDIRECT_FIELD_NAME, login as auth_login
from django.http import HttpResponse, HttpResponseRedirect

from common.mymako import render_mako_context
from account.utils import http_referer


class AccountSingleton(object):
    """
    单例基类
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls, *args, **kwargs)
        return cls._instance


class Account(AccountSingleton):
    """
    账号体系相关的基类Account
    提供通用的账号功能
    """

    _config = None
    env_code = ''

    def __init__(self):
        # 根据环境env_code加载账号配置文件
        try:
            curModule = __import__("account.%s" % self.env_code, globals(), {}, ['settings_account'])
            self._config = curModule.settings_account
        except Exception, e:
            curModule = __import__("account", globals(), {}, ['settings_account'])
            self._config = curModule.settings_account
            self._config.logger.error(u"加载%s环境下账户配置文件失败，使用了默认配置，异常信息：%s" % (self.env_code, e))

    def getConfig(self):
        return self._config

    # ======================此部分提供公共方法， 验证用户登录态相关==============================
    def login(self, request):
        """
        登录view使用的登录逻辑
        """
        # 生成登录成功的回调url
        callback_url = self.gen_jumpback_url(request)

        status = self.check_user_login_status(request, autoLogin=True)
        if status == 0:
            # 登录态有效， 如果是401过来的，则跳登录成功页， 否则直接跳callback url
            callback_url = '/accounts/login_success/' if request.GET.get('login_scode', '') == '401' else callback_url
            return HttpResponseRedirect(callback_url)
        elif status == -2:
            # cookie有效但是后台验证没通过，跳登录失败页， 提示用户可能原因
            return self.login_page(request)
        else:
            # cookie无效，跳转到登录页重新登录
            return self.redirectReLogin(request)

    def logout(self, request):
        """
        登出， 清除登录态， 然后跳转到referer页
        """
        auth.logout(request)
        refer_url = http_referer(request)
        return HttpResponseRedirect(refer_url)

    def login_page(self, request):
        """
        告知用户登录态无效， 需要重新登录的引导页
        """
        return render_mako_context(request, self._config.LOGIN_PAGE_TEMPLATE)

    def login_success(self, request):
        """
        登录成功的引导页
        """
        # 登录成功重新记录session
        if self.check_user_login_status(request) != 0:
            return render_mako_context(request, self._config.LOGIN_FAIL_TEMPLATE)

        return render_mako_context(request, self._config.LOGIN_SUCCESS_TEMPLATE)

    def check_failed(self, request):
        """
        功能开关检查失败
        """
        code = request.GET.get('code', '403')
        # func check失败的提示页面
        if code == 'func_check':
            res_page = '/account/func_check_failed.html'
        else:
            res_page = '/403.html'
        return render_mako_context(request, res_page)

    def check_user_login_status(self, request, autoLogin=True):
        """
        校验用户登录状态
        返回码：
        0 登录态有效
        -1 django登录态无效
        -2 django登录态有效，但后台登录验证无效，并已清除django登录态
        """
        if request.user.is_authenticated():
            return 0
        # 后台登录态有效， 直接返回0 登录态有效
        user = auth.authenticate(request=request)
        if user:
            if autoLogin:
                self.bk_login(request, user, getattr(user, 'full_info', {}))

            if not request.user.is_authenticated():
                return -1
            else:
                return 0
        else:
            # 后台登录态无效， 先清除django登录态， 再返回-2
            auth.logout(request)
            return -2

    def check_backend_login_status(self, request):
        """
        校验后台登录状态
        返回码：
        0 登录态有效
        -1 登录态无效
        """
        # 由于基类中不知道是哪个环境， 所以后台验证直接返回有效
        # 子类中覆盖此方法
        return True, None

    def bk_login(self, request, user, userInfo=None):
        """
        将用户登录态写入django session
        """
        auth_login(request, user)
        # 写入session
        request.session['username'] = user.username

        return True

    # ======================此部分提供公共方法， 处理response逻辑 =========================
    def handel_response(self, request, response):
        """
        登录验证中统一的response处理方法，统一处理 cookie、session 等
        """
        return response

    # ======================此部分提供跳转相关的方法======================================
    def gen_jumpback_url(self, request):
        """
        生成登录完成的跳转url
        """
        # 如果指定了回调url, 则使用请求中指定的
        cus_jump = request.GET.get(REDIRECT_FIELD_NAME, '').strip()
        if cus_jump != '':
            return cus_jump

        # 如果从管理页面跳来，则回调时加上admin/来跳回admin
        jump_url = self._config.LOGIN_REDIRECT_URL + ("admin/" if request.GET.get('is_admin', '') == '' else '')
        return jump_url

    def build_callback_url(self, request, jumpUrl):
        callback = request.build_absolute_uri()
        login_scheme, login_netloc = urlparse.urlparse(jumpUrl)[:2]
        current_scheme, current_netloc = urlparse.urlparse(callback)[:2]
        if ((not login_scheme or login_scheme == current_scheme) and
                (not login_netloc or login_netloc == current_netloc)):
            callback = request.get_full_path()
        return callback

    def _redirect_login(self, request, callback=None, loginUrl='', redirectFieldName="c_url"):
        """
        跳转到登录页面
        note: 适用场景为 1. DEV环境， TEST环境的非Ajax请求
        note: 2. 所有环境的首页非AJAX请求
        """
        loginUrl = self._config.LOGIN_URL if loginUrl == '' else loginUrl

        if callback is None:
            callback = self.build_callback_url(request, loginUrl)
        from django.contrib.auth.views import redirect_to_login
        return redirect_to_login(callback, loginUrl, redirectFieldName)

    def _redirect_unsingned(self, request, callback=None, jumpUrl='', redirectFieldName="req_url"):
        """
        跳转到登录失效页
        note: 适用场景为 1. 非Ajax并且非首页
        """
        jumpUrl = "http://%s%saccounts/login_page/" % (
            request.get_host(), self._config.SITE_URL) if jumpUrl == '' else jumpUrl
        if callback is None:
            callback = self.build_callback_url(request, jumpUrl)

        jumpUrl = "%s?%s=%s" % (jumpUrl, redirectFieldName, urllib.quote(callback))
        return HttpResponseRedirect(jumpUrl)

    def _redirect_401(self, request, callback=None, jumpUrl='', redirectFieldName="c_url"):
        """
        跳转到登录弹窗
        note: 适用场景为 1. Ajax登录失败
        """
        # ajax 登录成功后回调登录成功页面
        if callback is None:
            callback = "http://%s%saccounts/login_success/?is_ajax=1" % (request.get_host(), self._config.SITE_URL)
        # 登录弹出框
        if jumpUrl == '':
            jumpUrl = self._config.PLAIN_LOGIN_URL
            jumpUrl = jumpUrl + "&" if "?" in self._config.PLAIN_LOGIN_URL else '?'
            jumpUrl = "%s%s=%s" % (jumpUrl, redirectFieldName, callback)

        return HttpResponse(status=401, content=jumpUrl)

    def redirectReLogin(self, request, loginUrl='', redirectFieldName=REDIRECT_FIELD_NAME):
        """
        跳转到login页面
        """
        # ajax跳401
        if request.is_ajax():
            return self._redirect_401(request)
        # 首页，开发/测试环境， 跳登录页
        if self._config.RUN_MODE != 'PRODUCT' or request.path == '/':
            return self._redirect_login(request, loginUrl=loginUrl)
        # 非首页，跳登录失效
        return self._redirect_unsingned(request)
