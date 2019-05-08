# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from bkoauth.utils import transform_uin

from home_application.models import User

class LoginQQMiddleware(object):
    """qq记录"""

    def process_view(self, request, view, args, kwargs):
        """
        只能拦截process_view
        如果proces_request的话，request.user只能获得 "AnonymousUser" ，无法正确取得username

        """
        request_type = request.path.split("/")[1]
        if not request_type in ['login_qq', 'accounts']:
            # 除了注册和qq登陆页面，其他一律拦截
            uin = request.COOKIES.get('uin')
            if not uin:
                # 如果获取不到uin
                print(u'取不到uin')
                return HttpResponseRedirect(reverse('login_qq'))
            qq = transform_uin(uin)
            username = request.user
            if not User.objects.qq_exist(qq) and not User.objects.username_exist(username):
                # 如果未记录qq和username
                user = User()
                if user.save_qq(username=username, qq=qq):
                    # 增加记录成功
                    return HttpResponseRedirect(reverse('home'))
                else:
                    # 增加记录失败
                    print(u'增加记录失败')
                    return HttpResponseRedirect(reverse('login_qq'))




