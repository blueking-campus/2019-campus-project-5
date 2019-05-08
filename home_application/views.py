# -*- coding: utf-8 -*-
from common.mymako import render_mako_context
from django.views.decorators.http import require_http_methods
from django.core.urlresolvers import reverse
from django.http import (
    HttpResponse, JsonResponse
)

from home_application.models import (
    Award, Application, User
)
from home_application.decorators import (
    require_datetime_GET, require_int_GET, require_superuser
)



# 开发框架中通过中间件默认是需要登录态的，如有不需要登录的，可添加装饰器login_exempt【装饰器引入from account.decorators import login_exempt】
def login_qq(request):
    return render_mako_context(request, '/login_qq.html')


def api_login_qq(request):
    """手动添加qq"""
    qq = request.POST.get('qq');
    username = request.user
    print username, qq
    user = User()
    if user.save_qq(username=username, qq=qq):
        return HttpResponse(reverse('home'), status=302)
    else:
        return HttpResponse('保存失败', status=500)


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

    return render_mako_context(request, '/home_application/organizations.html')

@require_http_methods('GET')
def apply(request):
    """我的申报页面"""

    return render_mako_context(request, '/home_application/apply.html')

@require_http_methods('GET')
def review(request):
    """我的审核页面"""

    return render_mako_context(request, '/home_application/review.html')

@require_http_methods('GET')
def awards_review(request):
    """我的审核页面"""

    return render_mako_context(request, '/home_application/awards_review.html')

@require_http_methods('GET')
def clone(request):
    """我的审核页面"""

    return render_mako_context(request, '/home_application/clone.html')


@require_http_methods('GET')
@require_superuser
@require_int_GET('page')
@require_int_GET('page_size')
@require_datetime_GET('date_time')
def api_all_awards(request):

    page = request.GET.get('page', 1)
    page_size = request.GET.get('page_size', 10)
    name = request.GET.get('name', '')
    organization = request.GET.get('organization', '')
    stauts = request.GET.get('stauts', '')
    date_time = request.GET.get('date_time', '').replace('&nbsp;', ' ')

    awards = Award.objects.all(page=page, page_size=page_size, date_time=date_time, name=name, organization=organization, stauts=stauts)
    print awards
    return JsonResponse(awards)

