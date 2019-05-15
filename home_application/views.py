# -*- coding: utf-8 -*-
from common.mymako import render_mako_context
from django.views.decorators.http import require_http_methods
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.http import (
    HttpResponse, JsonResponse
)

from home_application.models import (
    Award, Application, User, Level, Organization
)
from home_application.decorators import (
    require_datetime_GET, require_int_GET, require_superuser
)
from home_application.utils import get_url_list


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
    router = get_url_list(['home'])
    data = {
        'viewable_awards': viewable_awards,
        'outdated_awards': outdated_awards,
        'router': router
    }
    return render_mako_context(request, '/home_application/home.html', data)


@require_http_methods('GET')
@require_superuser
def manage_awards(request):
    """奖项管理页面"""
    router = get_url_list(['manage', 'manage_awards'])
    manage_show_award = reverse('manage_show_award')
    manage_clone_award = reverse('manage_clone_award')
    manage_change_award = reverse('manage_change_award')
    api_delete_award_ = reverse('api_delete_award')
    api_awards_ = reverse('api_awards')
    data = {
        'router': router,
        'manage_show_award': manage_show_award,
        'manage_clone_award': manage_clone_award,
        'manage_change_award': manage_change_award,
        'api_delete_award': api_delete_award_,
        'api_awards': api_awards_,
    }
    return render_mako_context(request, '/home_application/manage_award.html', data)


@require_http_methods('GET')
@require_superuser
def manage_add_award(request):
    """添加奖项页面"""

    levels = Level.objects.all_list()
    organizations_ = Organization.objects.all_name_key()
    router = get_url_list(['manage', 'manage_awards', 'manage_add_award'])
    api = reverse('api_add_award')
    data = {
        'levels': levels,
        'organizations': organizations_,
        'api': api,
        'router': router
    }
    print data

    return render_mako_context(request, '/home_application/manage_award_edite.html', data)

@require_http_methods('GET')
@require_superuser
def manage_clone_award(request):
    """克隆奖项页面"""
    router = get_url_list(['manage', 'manage_awards'])
    data = {
        'router': router
    }
    return render_mako_context(request, '/home_application/manage_award_edite.html', data)


@require_http_methods('GET')
@require_superuser
def manage_change_award(request):
    """修改奖项页面"""
    print request.GET
    award__key = request.GET.get('award__key')
    if not award__key:
        return render_mako_context(request, '/404.html')
        # return HttpResponse('缺少参数award__key', status=404)
    levels = Level.objects.all_list()
    organizations_ = Organization.objects.all_name_key()
    try:
        award = Award.objects.get_values(key=award__key)
    except ObjectDoesNotExist, err:
        print err
        return render_mako_context(request, '/404.html')
    except IndexError, err:
        print err
        return render_mako_context(request, '/404.html')
    router = get_url_list(['manage', 'manage_awards', {'url_name': 'manage_change_award', 'kwargs': {'award__key': award__key}}])
    api = reverse('api_change_award')
    data = {
        'award': award,
        'levels': levels,
        'organizations': organizations_,
        'api': api,
        'router': router
    }
    return render_mako_context(request, '/home_application/manage_award_edite.html', data)


@require_http_methods('GET')
@require_superuser
def manage_show_award(request):
    """展示奖项页面"""
    print request.GET
    award__key = request.GET.get('award__key')
    if not award__key:
        return render_mako_context(request, '/404.html')
        # return HttpResponse('缺少参数award__key', status=404)
    levels = Level.objects.all_list()
    organizations_ = Organization.objects.all_name_key()
    try:
        award = Award.objects.get_values(key=award__key)
    except ObjectDoesNotExist, err:
        print err
        return render_mako_context(request, '/404.html')
    except IndexError, err:
        print err
        return render_mako_context(request, '/404.html')
    router = get_url_list(['manage', 'manage_awards', {'url_name': 'manage_show_award', 'kwargs': {'award__key': award__key}}])
    api = reverse('api_change_award')
    data = {
        'award': award,
        'levels': levels,
        'organizations': organizations_,
        'api': api,
        'router': router,
        'is_show': True,
    }
    return render_mako_context(request, '/home_application/manage_award_edite.html', data)


@require_http_methods('GET')
@require_superuser
def manage_organizations(request):
    """组织管理页面"""
    router = get_url_list(['manage', 'manage_organizations'])
    api_organizations_ = reverse('api_organizations')
    api_delete_organizations_ = reverse('api_delete_organizations')
    data = {
        'router': router,
        'api_delete_organizations': api_delete_organizations_,
        'api_organizations': api_organizations_,
    }
    return render_mako_context(request, '/home_application/manage_organizations.html', data)


@require_http_methods('GET')
def personal_apply(request):
    """我的申报页面"""

    return render_mako_context(request, '/home_application/apply.html')


@require_http_methods('GET')
def personal_review(request):
    """我的审核页面"""

    return render_mako_context(request, '/home_application/review.html')


@require_http_methods('GET')
def personal_awards_review(request):
    """我的审核页面"""

    return render_mako_context(request, '/home_application/awards_review.html')


@require_http_methods('POST')
@require_superuser
# @require_int_GET('start')
# @require_int_GET('length')
# @require_datetime_GET('datetime')
def api_all_organizations(request):
    """api 查询所有奖项"""
    draw = int(request.POST.get('draw'))
    page = int(request.POST.get('start', 1))+1
    page_size = int(request.POST.get('length', 10))
    organizations_ = Organization.objects.all(page=page, page_size=page_size)
    organizations_['draw'] = draw
    print organizations_
    return JsonResponse(organizations_)


@require_http_methods('GET')
@require_superuser
def api_all_awards(request):
    """api 查询所有奖项"""
    draw = int(request.GET.get('draw'))
    page = int(request.GET.get('start', 1))+1
    page_size = int(request.GET.get('length', 10))
    name = request.GET.get('name', '')
    organization = request.GET.get('organization', '')
    try:
        status = int(request.GET.get('status', 0))
    except ValueError, err:
        print err
        status = 0
    print status
    datetime = request.GET.get('datetime', '').replace('&nbsp;', ' ')

    awards_ = Award.objects.all(page=page, page_size=page_size, date_time=datetime, name=name, organization=organization, status=status)
    awards_['draw'] = draw
    return JsonResponse(awards_)


@require_http_methods('POST')
@require_superuser
def api_add_award(request):
    """api 增加award"""
    print request.POST

    request.POST['begin_time'] = request.POST['begin_time'].replace('&nbsp;', ' ')
    request.POST['end_time'] = request.POST['end_time'].replace('&nbsp;', ' ')
    is_active = request.POST.get('is_active')
    is_attached = request.POST.get('is_attached')
    if is_active == u'1':
        request.POST['is_active'] = True
    else:
        request.POST['is_active'] = False

    if is_attached == u'1':
        request.POST['is_attached'] = True
    else:
        request.POST['is_attached'] = False

    try:
        Award.create(request.POST)
    except ValueError, err:
        print err
        return HttpResponse(''.join(['添加失败', err]), content_type='text')
    except ObjectDoesNotExist, err:
        print err
        return HttpResponse(''.join(['添加失败', err]), content_type='text')
    else:
        return HttpResponse('添加成功', content_type='text')


@require_http_methods('POST')
@require_superuser
def api_change_award(request):
    """api 修改award"""
    print request.POST

    request.POST['begin_time'] = request.POST['begin_time'].replace('&nbsp;', ' ')
    request.POST['end_time'] = request.POST['end_time'].replace('&nbsp;', ' ')
    is_active = request.POST.get('is_active')
    is_attached = request.POST.get('is_attached')
    if is_active == u'1':
        request.POST['is_active'] = True
    else:
        request.POST['is_active'] = False

    if is_attached == u'1':
        request.POST['is_attached'] = True
    else:
        request.POST['is_attached'] = False

    try:
        Award.change(request.POST)
    except ValueError, err:
        print err
        return HttpResponse(''.join(['添加失败', err]), content_type='text')
    except ObjectDoesNotExist, err:
        print err
        return HttpResponse(''.join(['添加失败', err]), content_type='text')
    else:
        return HttpResponse('修改成功', content_type='text')


@require_http_methods('POST')
@require_superuser
def api_delete_award(request):
    """api 删除award"""
    key_list = request.POST.getlist('key[]');
    print request.POST
    print key_list
    try:
        Award.objects.delete(key_list)
    except Exception, err:
        print err
        return HttpResponse('删除失败', status=500)
    return HttpResponse('删除成功')


@require_http_methods('POST')
@require_superuser
def api_delete_award(request):
    """api 克隆奖项"""

    pass


@require_http_methods('POST')
@require_superuser
def api_delete_organizations(request):
    """api 删除organizations"""
    return HttpResponse('OK')
