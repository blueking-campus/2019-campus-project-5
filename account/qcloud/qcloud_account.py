# -*- coding: UTF-8 -*-
"""
账号体系相关的基类Account
"""
import urllib

from django.contrib.auth import get_user_model, REDIRECT_FIELD_NAME
from django.contrib import auth
from django.http import HttpResponseRedirect
from component.qcloud.shortcuts import get_client_by_request

from common.log import logger
from common.utils import html_escape, url_escape
from common.mymako import render_mako_context
from account.accounts import Account
from account.utils import is_url_in_domain, http_referer


class QcloudAccount(Account):
    """
    腾讯云版帐号登录相关
    """
    def __init__(self):
        self.env_code = 'qcloud'
        super(QcloudAccount, self).__init__()

    # ======================页面====================================================
    def check_failed(self, request):
        """
        功能开关检查失败
        """
        uin = request.COOKIES.get('uin', '')
        code = request.GET.get('code', '403')
        # func check失败的提示页面
        if code == 'func_check':
            res_page = '/account/func_check_failed.html'
        else:
            res_page = '/403.html'
        uin = self.transform_uin(uin)
        ctx = {'uin': uin}
        return render_mako_context(request, res_page, ctx)

    def logout(self, request):
        """
        登出， 清除登录态， 然后跳转到referer页
        """
        auth.logout(request)
        refer_url = http_referer(request)
        response = HttpResponseRedirect(refer_url)
        response.delete_cookie('openid', path=self._config.SITE_URL)
        response.delete_cookie('openkey', path=self._config.SITE_URL)
        return response

    def login_success(self, request):
        """
        qq登录成功页面
        """
        uin = request.COOKIES.get('uin', '')
        skey = request.COOKIES.get('skey', '')
        # 将uin转成qq号
        uin = self.transform_uin(uin)
        # 获取用户的 openid
        openid, openkey = self.get_openid_by_uin(request, uin, skey)

        if not self.verify_openid(request, openid, openkey):
            return render_mako_context(request, self._config.LOGIN_FAIL_TEMPLATE)

        # 原始请求是否为ajxa请求
        is_ajax = request.GET.get('is_ajax', '1')
        refer_url = request.GET.get('refer_url', '')
        redirect = request.GET.get("redirect", None)
        # 对参数做校验
        try:
            is_ajax = html_escape(is_ajax)
            # 回调url不存在或不在当前域名下则跳转到首页
            if not refer_url or not is_url_in_domain(refer_url):
                refer_url = self._config.S_URL
            else:
                refer_url = url_escape(refer_url)
        except:
            is_ajax = 1
            refer_url = self._config.S_URL

        if redirect:
            response = HttpResponseRedirect(refer_url)
            response.set_cookie('openid', openid, path=self._config.SITE_URL)
            response.set_cookie('openkey', openkey, path=self._config.SITE_URL)
            return response

        ctx = {'is_ajax': is_ajax, 'refer_url': refer_url}
        # 将用户头像和昵称放到session中
        response = render_mako_context(request, self._config.LOGIN_SUCCESS_TEMPLATE, ctx)
        response.set_cookie('openid', openid, path=self._config.SITE_URL)
        response.set_cookie('openkey', openkey, path=self._config.SITE_URL)
        return response

    # ======================此部分提供公共方法， 验证用户登录态相关==============================
    def check_user_login_status(self, request, autoLogin=True):
        """
        校验用户登录态
        登录态以cookie中的为准
        1）cookie中有效：
            a)session中无效，重新写session， 返回 0
            b)session中有效，返回0
        2）cookie中无效
            a)session中无效，返回-1
            b）sessoin中有效，
        0:登录态有效
        -1:登录态无效
        """
        # 取得openid openkey
        openid = request.GET.get('openid') or request.COOKIES.get('openid')
        openkey = request.GET.get('openkey') or request.COOKIES.get('openkey')
        if openid and openkey:
            request.COOKIES['openid'] = openid
            request.COOKIES['openkey'] = openkey
        # 校验登录态
        result, data = self.verify_qcloud_user(request, openid, openkey)
        if result:
            is_bk_login = True
            # 判断 session中的登录态是否有效
            if request.user.is_authenticated():
                # 判断session 中 用户 信息和cookie中的用户信息是否一致
                if data.get('openid', '') != request.user.username:
                    # 原有账号退出登录
                    auth.logout(request)
                else:
                    # 用户登录信息正确， 不需要再重新登录
                    is_bk_login = False
            if is_bk_login:
                user = auth.authenticate(request=request)
                self.bk_login(request, user, getattr(user, 'full_info', {}))
            # 登录态有效返回
            return 0
        else:
            # 清除 session 中的登录态
            if request.user.is_authenticated():
                # 后台登录态无效， 先清除 session登录态
                auth.logout(request)
            return -1

    def check_backend_login_status(self, request):
        """
        校验后台登录状态
        返回码：
        0 登录态有效
        -1 登录态无效
        """
        # 取得openid openkey
        openid = request.GET.get('openid') or request.COOKIES.get('openid')
        openkey = request.GET.get('openkey') or request.COOKIES.get('openkey')
        if openid and openkey:
            request.COOKIES['openid'] = openid
            request.COOKIES['openkey'] = openkey

        # 校验登录态
        result, data = self.verify_qcloud_user(request, openid, openkey)

        if not result:
            return False, {}

        # 检查此用户是否在django用户表里
        userName = data.get('openid', '')
        user_model = get_user_model()
        try:
            user = user_model.objects.get(username=userName)
        except user_model.DoesNotExist:
            # 第一次登录的时候要新建一个user
            user = user_model(username=userName)
            user.save()

        setattr(user, 'full_info', data)
        return True, user

    def verify_qcloud_user(self, request, openid, openkey):
        if openid == '' or openkey == '' or openid is None or openkey is None:
            return False, {}
        # 验证通过， 拉取云用户信息
        userInfo = self.query_userinfo(request, openid, openkey)
        if not userInfo:
            return False, {}
        return True, userInfo

    def verify_openid(self, request, openid, openkey):
        try:
            query_param = {'openid': openid, 'openkey': openkey}
            client = get_client_by_request(request)

            resp = client.oidb.verify_openid_openkey(query_param)
            result = resp.get('result', False)
            if result:
                return True
            message = resp.get('message', '')
            logger.error(u"调用组件 verify_cookie 出错, openid:%s, openkey:%s, message:%s, resp:%s" % (
                openid, openkey, message, resp))
            return False
        except Exception, e:
            logger.error(u"验证用户（openid：%s）cookie的有效性出错:%s" % (openid, e))
            return False

    def query_userinfo(self, request, openid, openkey):
        """
        获取用户信息包括用户昵称和头像
        return: {'nick_name': nick_name, 'avatar_url': avatar_url}
        """
        userinfo = {'openid': openid, 'openkey': openkey}
        client = get_client_by_request(request)
        resp = client.oidb.get_user_info({'openid': openid, 'openkey': openkey})
        result = resp.get('result', False)
        if not result:
            message = resp.get('message', '')
            logger.error(u"调用组件 get_user_info 出错，openid:%s, message:%s, resp：%s" % (openid, message, resp))
            return False

        data = resp.get('data', {})
        userinfo['nick_name'] = data.get('nick_name', '')
        userinfo['avatar_url'] = data.get('avatar_url', '')
        return userinfo

    def bk_login(self, request, user, userInfo):
        """
        登录
        """
        super(QcloudAccount, self).bk_login(request, user)
        request.session['openid'] = userInfo.get('openid', '')
        request.session['openkey'] = userInfo.get('openkey', '')
        request.session['nick'] = userInfo.get('nick_name', '')
        request.session['avatar'] = userInfo.get('avatar_url', '')
        return True

    def get_openid_by_uin(self, request, uin, skey):
        """
        获取用户的 openid，openkey
        return: (openid, openkey)
        todo: 调用组件接口
        """
        openid = ''
        openkey = ''
        if uin == '' or skey == '':
            return (openid, openkey)

        try:
            query_param = {
                'uin': uin,
                'skey': skey,
            }
            client = get_client_by_request(request)
            resp = client.oidb.get_openid_openkey(query_param)
            result = resp.get('result', False)
            if result:
                data = resp.get('data', {})
                openid = data.get('openid', '')
                openkey = data.get('openkey', '')
            else:
                message = resp.get('message', '')
                logger.error(u"调用组件 get_open_id_key 出错, uin:%s, skey:%s, message:%s, resp:%s" % (
                    uin, skey, message, resp))
        except Exception, e:
            logger.error(u"获取用户的（%s）的 openid 异常:%s" % (uin, e))
        return (openid, openkey)

    # ======================此部分提供公共方法， 处理response逻辑 =========================
    def handel_response(self, request, response):
        """
        登录验证中统一的response处理方法，统一处理 cookie、session 等
        """
        # 获取 openid openkey
        openid = request.GET.get('openid', '')
        openkey = request.GET.get('openkey', '')
        if openid and openkey:
            # 验证 openid 和 openkey
            openid = html_escape(openid)
            openkey = html_escape(openkey)
            response.set_cookie('openid', openid, path=self._config.SITE_URL)
            response.set_cookie('openkey', openkey, path=self._config.SITE_URL)
        return response

    # ======================跳转相关 =========================
    def _redirect_console(self, request):
        """
        跳转到登录页面
        note: 适用场景为 1. DEV环境， TEST环境的非Ajax请求
        note: 2. 所有环境的首页非AJAX请求
        """
        refer_url = self._config.S_URL if request.is_ajax() else request.build_absolute_uri()
        # 登录成功后跳转到首页(TODO 刷新当前的页面)
        qq_login_page = "%s/accounts/ptlogin_page?app_code=%s&refer_url=%s" % (
            self._config.BK_URL, self._config.APP_CODE, urllib.quote(refer_url))
        return HttpResponseRedirect(qq_login_page)

    def redirectReLogin(self, request, loginUrl='', redirectFieldName=REDIRECT_FIELD_NAME):
        """
        跳转到login页面
        """
        # ajax跳401
        if request.is_ajax():
            callback = self._config.CROSS_PREFIX + "%s/accounts/login_success/?is_ajax=1" % self._config.S_URL
            return self._redirect_401(request, callback=callback)

        if self._config.RUN_MODE == 'PRODUCT':
            return self._redirect_console(request)

        # 首页，开发/测试环境， 跳登录页
        # if request.path == '/':
        callback = urllib.quote(self.build_callback_url(request, loginUrl))
        callback = self._config.CROSS_PREFIX + urllib.quote("%s/accounts/login_success/?redirect=1&refer_url=%s" % (
            self._config.S_URL, callback))
        callback = urllib.quote(callback)
        return self._redirect_login(request, callback=callback, loginUrl=loginUrl)

    def transform_uin(self, uin):
        """
        将腾讯云的uin转换为字符型的qq号
        就是去掉第一个字符然后转为整形
        """
        try:
            uin = int(uin[1:]) if uin else ''
        except Exception, e:
            self._config.logger.error(u"uin转换出错：%s,uin:%s" % (e, uin))
            return ''
        else:
            return str(uin)
