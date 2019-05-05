# -*- coding: utf-8 -*-
import json

from common.mymako import render_mako_context
from django.views.decorators.http import require_http_methods

from home_application.models import Award
from home_application.models import Application

# 开发框架中通过中间件默认是需要登录态的，如有不需要登录的，可添加装饰器login_exempt【装饰器引入from account.decorators import login_exempt】
@require_http_methods('GET')
def home(request):
    """
    首页
    """
    viewable_awards = Award.objects.all_by_username(username=request.user, is_active=True)
    outdated_awards = Application.objects.awarded(username=request.user)
    data = {'viewable_awards': viewable_awards,
            'outdated_awards': outdated_awards}
    return render_mako_context(request, '/home_application/home.html', data)

@require_http_methods('GET')
def personal(request):
    my_apply_awards = Award.objects.all_by_username(request.user)
    my_review_awrds = Award.objects.all_by_username(request.user)
    data = {'my_apply_awards': my_apply_awards,
            'my_review_awrds': my_review_awrds,
            'username': request.user}
    return render_mako_context(request, '/home_application/personal.html',data)

@require_http_methods('GET')
def manage(request):
    return render_mako_context(request, '/home_application/manage.html')
