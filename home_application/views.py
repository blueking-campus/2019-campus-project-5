# -*- coding: utf-8 -*-
from common.mymako import render_mako_context
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse, JsonResponse

from home_application.models import Award
from home_application.models import Application
from home_application.decorators import require_superuser
from home_application.utils import is_vaild_datetime
from home_application.utils import is_int

# 开发框架中通过中间件默认是需要登录态的，如有不需要登录的，可添加装饰器login_exempt【装饰器引入from account.decorators import login_exempt】
@require_http_methods('GET')
def home(request):
    """首页"""
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
@require_superuser
def manage(request):
    return render_mako_context(request, '/home_application/manage.html')


@require_http_methods('GET')
@require_superuser
def awards(request):
    """奖项管理页面"""

    return render_mako_context(request, '/home_application/manage_award.html')


@require_http_methods('GET')
@require_superuser
def organizations(request):
    """组织管理页面"""

    return render_mako_context(request, '/home_application/manage.html')


@require_http_methods('GET')
@require_superuser
def get_all_awards(request):

    page = request.GET.get('page', None)
    page_size = request.GET.get('page_size', 10)
    name = request.GET.get('name', None)
    organization = request.GET.get('organization', None)
    stauts = request.GET.get('stauts', None)
    date_time = request.GET.get('date_time', None)


    if not is_int(page) and page:
        return HttpResponse('页数必须为整数')
    else:
        page = int(page)

    if not is_int(page_size) and page_size:
        return HttpResponse('页页面大小必须为整数')
    else:
        page = int(page_size)

    if (not is_vaild_datetime(date_time)) and date_time:
        # datetime不为空且不是datetime格式
        return HttpResponse('日期格式不正确')

    awards = Award.objects.all(page=page, page_size=page_size, date_time=date_time, name=name, organization=organization, stauts=stauts)
    print awards
    return JsonResponse(awards)

