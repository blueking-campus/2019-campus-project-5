# -*- coding: utf-8 -*-
from common.mymako import render_mako_context
from django.views.decorators.http import require_http_methods
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.http import  HttpResponse, JsonResponse

from home_application.models import Award, Application, User, Level, Organization, Application, Accessory
from home_application.decorators import require_datetime_GET, require_int_GET, require_superuser
from home_application.utils import get_url_list

from home_application.utils import DateJSONEncoder, generateUUID, get_file


# 开发框架中通过中间件默认是需要登录态的，如有不需要登录的，可添加装饰器login_exempt【装饰器引入from account.decorators import login_exempt】
def login_qq(request):
    return render_mako_context(request, '/login_qq.html')


def api_login_qq(request):
    """手动添加qq"""
    qq = request.POST.get('qq');
    username = request.user.username
    print username, qq
    user = User()
    if user.save_qq(username=username, qq=qq):
        return HttpResponse(reverse('home'), status=302)
    else:
        return HttpResponse('保存失败', status=500)


@require_http_methods('GET')
def home(request):
    """首页"""
    viewable_awards = Award.objects.all_by_username(username=request.user.username, is_active=True)
    outdated_awards = Application.objects.awarded(username=request.user.username)
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
    manage_show_award_ = reverse('manage_show_award')
    manage_clone_award_ = reverse('manage_clone_award')
    manage_change_award_ = reverse('manage_change_award')
    api_delete_award_ = reverse('api_delete_award')
    api_awards_ = reverse('api_awards')
    data = {
        'router': router,
        'manage_show_award': manage_show_award_,
        'manage_clone_award': manage_clone_award_,
        'manage_change_award': manage_change_award_,
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

    return render_mako_context(request, '/home_application/manage_edit_award.html', data)

@require_http_methods('GET')
@require_superuser
def manage_clone_award(request):
    """克隆奖项页面"""
    router = get_url_list(['manage', 'manage_awards'])
    data = {
        'router': router
    }
    return render_mako_context(request, '/home_application/manage_edit_award.html', data)


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
    return render_mako_context(request, '/home_application/manage_edit_award.html', data)


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
    return render_mako_context(request, '/home_application/manage_edit_award.html', data)


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
def personal_review(request):
    """我的审核页面"""
    router = get_url_list(['personal', 'personal_review'])
    api_my_review_ = reverse('api_my_review')
    pass_award_ = reverse('pass_award')
    reject_award_ = reverse('reject_award')
    give_award_ = reverse('give_award')
    data = {
        'router': router,
        'api_my_review': api_my_review_,
        'pass_award': pass_award_,
        'reject_award': reject_award_,
        'give_award': give_award_,
    }
    return render_mako_context(request, '/home_application/personal_review.html', data)

@require_http_methods('GET')
def pass_award(request):
    application__key = request.GET.get('application__key')
    if not application__key:
        # apply_key/award_key为空
        print u'参数为空'
        return render_mako_context(request, '/404.html')
    if not Application.objects.is_exist(key=application__key):
        # 不存在该申请
        print u'不存在该申请'
        return render_mako_context(request, '/404.html')
    try:
        application_ = Application.objects.get_values(application__key)
        print application_
    except ObjectDoesNotExist, err:
        print err
        return render_mako_context(request, '/404.html')
    Application.objects.filter(key=application__key).update(status=2)
    return HttpResponse('已经通过')

@require_http_methods('GET')
def reject_award(request):
    application__key = request.GET.get('application__key')
    if not application__key:
        # apply_key/award_key为空
        print u'参数为空'
        return render_mako_context(request, '/404.html')
    if not Application.objects.is_exist(key=application__key):
        # 不存在该申请
        print u'不存在该申请'
        return render_mako_context(request, '/404.html')
    try:
        application_ = Application.objects.get_values(application__key)
        print application_
    except ObjectDoesNotExist, err:
        print err
        return render_mako_context(request, '/404.html')
    Application.objects.filter(key=application__key).update(status=1)
    return HttpResponse('已经驳回')

@require_http_methods('GET')
def give_award(request):
    application__key = request.GET.get('application__key')

    if not application__key:
        # apply_key/award_key为空
        print u'参数为空'
        return render_mako_context(request, '/404.html')
    if not Application.objects.is_exist(key=application__key):
        # 不存在该申请
        print u'不存在该申请'
        return render_mako_context(request, '/404.html')

    try:
        application_ = Application.objects.get_values(application__key)
    except ObjectDoesNotExist, err:
        print err
        return render_mako_context(request, '/404.html')

    router = get_url_list(['personal', 'personal_review'])
    api_give_award_ = reverse('api_give_award')
    data = {
        'application': application_['application'],
        'award': application_['award'],
        'router': router,
        'api_give_award': api_give_award_,
    }
    return render_mako_context(request, '/home_application/give_award.html', data)

@require_http_methods('GET')
def api_give_award(request):
    application__key = request.GET.get('application_key')
    print 'key=',application__key
    is_give = request.GET.get('is_give')
    pingyu = request.GET.get('pingyu')
    if is_give == '1':
        Application.objects.filter(key=application__key).update(status=4)
        Application.objects.filter(key=application__key).update(pingyu=pingyu)
    else:
        Application.objects.filter(key=application__key).update(status=3)
        Application.objects.filter(key=application__key).update(pingyu=pingyu)

    print is_give,type(is_give), is_give == '1'
    return HttpResponse('提交成功')

@require_http_methods('GET')
def personal_apply(request):
    """我的申报页面"""
    router = get_url_list(['personal', 'personal_apply'])
    api_my_apply_ = reverse('api_my_apply')
    personal_change_apply_ = reverse('personal_change_apply')
    personal_show_apply_ = reverse('personal_show_apply')
    personal_reapply_ = reverse('personal_reapply')
    data = {
        'router': router,
        'api_my_apply': api_my_apply_,
        'personal_change_apply': personal_change_apply_,
        'personal_show_apply': personal_show_apply_,
        'personal_reapply': personal_reapply_,
    }
    return render_mako_context(request, '/home_application/personal_apply.html', data)


@require_http_methods('GET')
def personal_change_apply(request):
    """修改申请页面"""
    application__key = request.GET.get('application__key')
    username = request.user.username

    if not application__key:
        # apply_key/award_key为空
        print u'参数为空'
        return render_mako_context(request, '/404.html')
    if not Application.objects.is_exist(key=application__key):
        # 不存在该申请
        print u'不存在该申请'
        return render_mako_context(request, '/404.html')
    if not Application.objects.can_edit(username=username, key=application__key):
        # 不能编辑该奖项
        return render_mako_context(request, '/403.html')

    try:
        application_ = Application.objects.get_values(application__key)
    except ObjectDoesNotExist, err:
        print err
        return render_mako_context(request, '/404.html')

    router = get_url_list(['personal', 'personal_apply', 'personal_change_apply'])
    api_change_apply_ = reverse('api_change_apply')
    data = {
        'application': application_['application'],
        'award': application_['award'],
        'router': router,
        'api_chang_apply': api_change_apply_,
    }
    return render_mako_context(request, '/home_application/application_edit_apply.html', data)


@require_http_methods('GET')
def personal_reapply(request):
    """重新申请页面"""
    application__key = request.GET.get('application__key')
    username = request.user.username

    if not application__key:
        # apply_key/award_key为空
        print u'参数为空'
        return render_mako_context(request, '/404.html')
    if not Application.objects.is_exist(key=application__key):
        # 不存在该申请
        print u'不存在该申请'
        return render_mako_context(request, '/404.html')
    if not Application.objects.can_edit(username=username, key=application__key):
        # 不能编辑该奖项
        return render_mako_context(request, '/403.html')

    try:
        application_ = Application.objects.get_values(application__key)
    except ObjectDoesNotExist, err:
        print err
        return render_mako_context(request, '/404.html')

    router = get_url_list(['personal', 'personal_apply', 'personal_change_apply'])
    api_reapply_ = reverse('api_reapply')
    data = {
        'application': application_['application'],
        'award': application_['award'],
        'router': router,
        'api_chang_apply': api_reapply_,
    }
    return render_mako_context(request, '/home_application/application_edit_apply.html', data)


@require_http_methods('GET')
def personal_show_apply(request):
    """查看申请页面"""
    application__key = request.GET.get('application__key')

    if not application__key:
        # apply_key/award_key为空
        print u'参数为空'
        return render_mako_context(request, '/404.html')
    if not Application.objects.is_exist(key=application__key):
        # 不存在该申请
        print u'不存在该申请'
        return render_mako_context(request, '/404.html')

    try:
        application_ = Application.objects.get_values(application__key)
    except ObjectDoesNotExist, err:
        print err
        return render_mako_context(request, '/404.html')

    router = get_url_list(['personal_show_apply'])
    api_change_apply_ = reverse('api_change_apply')
    print application_
    data = {
        'application': application_['application'],

        'award': application_['award'],
        'router': router,
        'api_chang_apply': api_change_apply_,
    }
    return render_mako_context(request, '/home_application/application_show_apply.html', data)



@require_http_methods('GET')
def application_apply(request):
    """奖项申请页面"""
    award_key = request.GET.get('award_key')
    username = request.user.username
    if not Award.objects.can_apply(username=username, award_key=award_key):
        # 不能申请该奖项
        return render_mako_context(request, '/403.html')
    try:
        award = Award.objects.get_values(award_key)
    except ObjectDoesNotExist, err:
        print err
        return HttpResponse('不存在该奖项', status=400)
    else:
        router = get_url_list(['application_apply'])
        api_apply_ = reverse('api_apply')
        data = {
            'award': award,
            'router': router,
            'api_apply': api_apply_,
        }
        return render_mako_context(request, '/home_application/application_apply.html', data)


@require_http_methods('GET')
@require_superuser
# @require_int_GET('start')
# @require_int_GET('length')
# @require_datetime_GET('datetime')
def api_all_organizations(request):
    """api 查询所有奖项"""
    draw = int(request.GET.get('draw'))
    page = int(request.GET.get('start', 1)) + 1
    page_size = int(request.GET.get('length', 10))
    organizations_ = Organization.objects.all_search(page=page, page_size=page_size)
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

    awards_ = Award.objects.all_search(page=page, page_size=page_size, date_time=datetime, name=name, organization=organization, status=status)
    awards_['draw'] = draw
    return JsonResponse(awards_)

@require_http_methods('GET')
@require_superuser
def api_add_organizations(request):
    zu_zhi = request.GET.get('zu_zhi')
    zu_zhang = request.GET.get('zu_zhang')
    zu_yuan = request.GET.get('zu_yuan')
    print zu_zhi,zu_zhang,zu_yuan,request.GET

    Organization.objects.create(name=zu_zhi, reviewer=zu_zhang, applicant=zu_yuan, manager=zu_zhang, is_deleted=False, key=generateUUID())
    print '成功'
    return HttpResponse('添加成功', content_type='text')

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

    if Award.objects.name_exist(request.POST.get('name')):
        return HttpResponse('已存在同名奖项', status=400)

    try:
        Award.create(request.POST)
    except ValueError, err:
        print err
        return HttpResponse('添加失败,保存奖项失败', content_type='text', status=400)
    except ObjectDoesNotExist, err:
        print err
        return HttpResponse('添加失败，不存在该级别或者所属组织', content_type='text', status=400)
    else:
        path = reverse('manage_awards')
        return HttpResponse(path, content_type='text', status=302)


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
        return HttpResponse('修改失败,保存奖项失败', content_type='text')
    except ObjectDoesNotExist, err:
        print err
        return HttpResponse('修改失败，不存在该级别或者所属组织', content_type='text')
    else:
        return HttpResponse('修改成功', content_type='text')


@require_http_methods('POST')
@require_superuser
def api_delete_award(request):
    """api 删除award"""
    key_list = request.POST.getlist('key[]')
    print request.POST
    print key_list
    try:
        Award.objects.logic_delete(key_list)
    except Exception, err:
        print err
        return HttpResponse('删除失败', status=500)
    return HttpResponse('删除成功')


@require_http_methods('POST')
@require_superuser
def api_delete_organizations(request):
    """api 删除organizations"""
    key_list = request.POST.getlist('key[]')
    print key_list
    try:
        Organization.objects.logic_delete(key_list)
    except Exception, err:
        print err
        return HttpResponse('删除失败', status=500)
    return HttpResponse('删除成功')

@require_http_methods('GET')
def api_my_review(request):
    """api 查询所有我的审核"""
    username = request.user.username
    draw = int(request.GET.get('draw'))
    page = int(request.GET.get('start', 1))+1
    page_size = int(request.GET.get('length', 10))

    my_review = Application.objects.my_review(username=username, page=page, page_size=page_size)
    my_review['draw'] = draw
    print '###view: my_apply:', my_review
    return JsonResponse(my_review)

@require_http_methods('GET')
def api_my_apply(request):
    """api 查询所有我的申请"""
    username = request.user.username
    draw = int(request.GET.get('draw'))
    page = int(request.GET.get('start', 1))+1
    page_size = int(request.GET.get('length', 10))
    name = request.GET.get('name', '')

    try:
        status = int(request.GET.get('status'))
    except ValueError, err:
        print err
        status = -1
    datetime = request.GET.get('datetime', '').replace('&nbsp;', ' ')

    my_apply = Application.objects.my_apply(username=username, page=page, page_size=page_size, date_time=datetime, name=name, status=status)
    my_apply['draw'] = draw
    print '###view: my_apply:', my_apply
    return JsonResponse(my_apply)


@require_http_methods('POST')
def api_change_apply(request):
    """api 修改我的申请"""
    username = request.user.username
    application_key = request.POST.get('application_key')
    applicant = request.POST.get('applicant')
    introduction = request.POST.get('introduction')
    file = request.FILES.get("file", None)

    if not application_key or not applicant or not introduction:
        # apply_key/award_key为空
        print u'参数为空'
        return HttpResponse('参数错误', status=404)
    if not Application.objects.is_exist(key=application_key):
        # 不存在该申请
        print u'不存在该申请'
        return HttpResponse('不存在该申请', status=404)
    if not Application.objects.can_edit(username=username, key=application_key):
        # 不能编辑该奖项
        return HttpResponse('无法编辑该奖项', status=403)
    try:
        Application.change(key=application_key, introduction=introduction, applicant=applicant, file=file)
    except ObjectDoesNotExist, err:
        print err
        return HttpResponse('不存在该申请', status=400)
    except ValueError, err:
        print err
        return HttpResponse('保存修改失败', status=500)
    else:
        res = reverse('personal_apply')
        return HttpResponse(res, status=302)


@require_http_methods('POST')
def api_reapply(request):
    """api 重新申请"""
    username = request.user.username
    application_key = request.POST.get('application_key')
    applicant = request.POST.get('applicant')
    introduction = request.POST.get('introduction')
    file = request.FILES.get("file", None)

    if not application_key or not applicant or not introduction:
        # apply_key/award_key为空
        print u'参数为空'
        return HttpResponse('参数错误', status=404)
    if not Application.objects.is_exist(key=application_key):
        # 不存在该申请
        print u'不存在该申请'
        return HttpResponse('不存在该申请', status=404)
    if not Application.objects.can_edit(username=username, key=application_key):
        # 不能编辑该奖项
        return HttpResponse('无法编辑该奖项', status=403)
    try:
        Application.reapply(key=application_key, introduction=introduction, applicant=applicant, file=file)
    except ObjectDoesNotExist, err:
        print err
        return HttpResponse('不存在该申请', status=400)
    except ValueError, err:
        print err
        return HttpResponse('保存修改失败', status=500)
    else:
        res = reverse('personal_apply')
        return HttpResponse(res, status=302)


@require_http_methods('POST')
def api_apply(request):
    """api 申请奖项"""
    award_key = request.POST.get('award_key')
    applicant = request.POST.get('applicant')
    introduction = request.POST.get('introduction')
    file = request.FILES.get("file", None)
    username = request.user.username

    print request.POST
    print username
    print award_key
    if not Award.objects.can_apply(username=username, award_key=award_key):
        # 不能申请该奖项
        return HttpResponse('无法申请该奖项', status=403)

    try:
        Application.apply(username=username, award_key=award_key, applicant=applicant, introduction=introduction, file=file)
    except ObjectDoesNotExist, err:
        print err
        return HttpResponse('申报失败，不存在该奖项', status=400)
    except ValueError, err:
        print err
        return HttpResponse('申报失败，保存内容失败', status=400)
    except RuntimeError, err:
        print err
        return HttpResponse('申报失败，你已经申报了该奖项', status=400)
    else:
        res = reverse('personal_apply')
        return HttpResponse(res, status=302)


@require_http_methods('GET')
def api_download_file(request):
    key = request.GET.get('key')
    try:
        access = Accessory.objects.get(key=key)
    except ObjectDoesNotExist, err:
        print err
        return render_mako_context('/404.html')
    else:
        res = get_file(access.key+'--'+access.name)
        print res
        file_ = res.get('Body').get_raw_stream()
        # 设定文件头，这种设定可以让任意文件都能正确下载，而且已知文本文件不是本地打开
        response = HttpResponse(file_, content_type='APPLICATION/OCTET-STREAM')
        # 设定传输给客户端的文件名称
        response['Content-Disposition'] = 'attachment; filename=%s' % access.name
        return response

