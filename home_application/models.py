# -*- coding: utf-8 -*-
import json
import datetime

from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger

from home_application.utils import DateJSONEncoder


class User(models.Model):
    """用户关联表"""
    username = models.CharField(max_length=64, verbose_name=u'用户名', unique=True)
    qq = models.CharField(max_length=64, verbose_name=u'qq号码', unique=True)

    class Mate:
        verbose_name = u'用户关联'
        verbose_name_plural = verbose_name

    def get_qq(self):
        """获取qq"""
        return self.qq


class Level(models.Model):
    """奖项级别"""
    name = models.CharField(max_length=64, verbose_name=u'级别', unique=True)
    class Mate:
        verbose_name = u'级别'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class OrganizationManager(models.Manager):
    """组织管理类"""

    def creat(self, name, reviwer, applicant, manager):
        """创建组织"""
        reviwer = '' if reviwer is None else reviwer
        applicant = '' if applicant is None else applicant
        if name:
            # name不为空或None
            try:
                with transaction.atomic():
                    Organization(name=name, reviwer=reviwer, applicant=applicant, manager=manager).save()
            except Exception:
                # 数据库操作失败，创建组织失败
                return False
            else:
                # 创建组织成功
                return True
        else:
            # name为空或None，创建组织失败
            return False

    def all(self, page, page_size):
        """查询所有未逻辑删除的组织"""
        orgs = super(models.Manager, self).filter(is_deleted=False)
        response = {}
        paginator = Paginator(orgs, page_size)
        response['total'] = paginator.count
        try:
            orgs = paginator.page(page)
        except PageNotAnInteger:
            orgs = paginator.page(1)
        except EmptyPage:
            orgs = paginator.page(paginator.num_pages)
        # 格式化数据
        data = orgs.values('key', 'name', 'reviewer', 'applicant', 'manager', 'created_time')
        data = json.dumps(list(data), cls=DateJSONEncoder)
        data = json.loads(data)
        response['organizations'] = data
        return response


class Organization(models.Model):
    """组织"""
    name = models.CharField(max_length=64, verbose_name=u'组织名称')
    reviewer = models.TextField(verbose_name=u'负责人员', blank=True)
    applicant = models.TextField(verbose_name=u'申请人', blank=True)

    key = models.CharField(max_length=64, verbose_name=u'组织标识', unique=True)
    manager = models.CharField(max_length=64, verbose_name=u'更新人')
    update_time = models.DateTimeField(verbose_name=u'更新时间', auto_now=True)
    created_time = models.DateTimeField(verbose_name=u'申报时间', auto_now_add=True)
    is_deleted = models.BooleanField(verbose_name=u'逻辑删除', default=False)

    objects = OrganizationManager()

    class Mate:
        verbose_name = u'组织'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def logical_delete(self):
        """逻辑删除组织"""
        try:
            with transaction.atomic():
                self.is_deleted = True
                self.save()
        except Exception:
            return False
        else:
            return True

    def updata(self, name, reviwer, applicant, manager):
        """修改组织信息"""
        try:
            with transaction.atomic():
                self.name = name
                self.reviewer = reviwer
                self.applicant = applicant
                self.manager = manager
                self.save()
        except Exception:
            return False
        else:
            return True


class AwardManager(models.Manager):
    """奖项管理类"""

    def all(self, name, organization, stauts, date_time, page=1, page_size=10):
        """查询所有未逻辑删除的奖项"""

        # 所有未逻辑删除的奖项
        awards = super(models.Manager, self).filter(is_deleted=False)

        if name:
            # 模糊查询奖项名
            awards = awards.filter(name__icontains=name)
        if organization:
            # 模糊查询组织名
            awards = awards.filter(organization__name__icontains=organization)
        if stauts == 1:
            # 查询奖项状态
            # status: (0, 不限)， (1, 过期), (2, 生效)
            awards = awards.filter(is_active=False)
        elif stauts == 2:
            awards = awards.filter(is_active=True)
        if date_time:
            # 查询时间
            date_time = datetime.datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S")
            awards = awards.filter(begin_time__lte=date_time, end_time__gte=date_time)

        # 分页
        response = {}
        paginator = Paginator(awards, page_size)
        response['total'] = paginator.count
        response['page_size'] = page_size
        response['page'] = page
        try:
            awards = paginator.page(page).object_list
        except PageNotAnInteger:
            awards = paginator.page(1).object_list
        except EmptyPage:
            awards = paginator.page(paginator.num_pages).object_list

        # 格式化数据
        awards.extra(select={'status': "IF(is_active, '生效中', '已过期')"})
        data = awards.values('key', 'requirement', 'level__name',
                            'organization__name', 'status', 'begin_time',
                            'end_time', 'apply_number', 'awarded_number')
        data = json.dumps(list(data), cls=DateJSONEncoder)
        data = json.loads(data)
        response['awards'] = data
        return response

    def all_by_username(self, username, is_active=True):
        """通过username查询该username可参加的奖项"""
        try:
            qq = User.objects.get(username=username).get_qq()
        except ObjectDoesNotExist, err:
            print err
            return []
        awards = super(models.Manager, self).filter(organization__applicant__contains=qq, is_active=is_active)
        # 格式化数据
        # awards.extra(select={'status': "if is_active '生效中' else '已过期')"})
        data = awards.values('key', 'name', 'requirement', 'level__name',
                            'organization__name', 'is_active', 'begin_time',
                            'end_time', 'apply_number', 'awarded_number')
        data = json.dumps(list(data), cls=DateJSONEncoder)
        data = json.loads(data)
        return data

    def creat(self):
        """创建奖项"""
        pass


class Award(models.Model):
    """奖项"""
    name = models.CharField(max_length=64, verbose_name=u'奖项名称')
    requirement = models.TextField(verbose_name=u'评选条件', blank=True)
    level = models.ForeignKey(to=Level, verbose_name=u'奖项级别', on_delete=models.CASCADE)
    organization = models.ForeignKey(to=Organization, verbose_name=u'所属组织', on_delete=models.CASCADE)
    begin_time = models.DateTimeField(verbose_name=u'开始时间')
    end_time = models.DateTimeField(verbose_name=u'结束时间')
    is_attached = models.BooleanField(verbose_name=u'是否有附件')
    IS_ACTIVE_CHOICES = (
        (True, u'生效中'),
        (False, u'已过期')
    )
    is_active = models.BooleanField(verbose_name=u'是否生效', choices=IS_ACTIVE_CHOICES)

    apply_number = models.IntegerField(verbose_name=u'申请人数', default=0)
    awarded_number = models.IntegerField(verbose_name=u'获奖人数', default=0)
    key = models.CharField(max_length=64, verbose_name=u'奖项标识', unique=True)
    created_time = models.DateTimeField(verbose_name=u'创建时间', auto_now_add=True)
    is_deleted = models.BooleanField(verbose_name=u'逻辑删除', default=False)

    objects = AwardManager()

    class Mate:
        verbose_name = u'奖项'
        verbose_name_plural = verbose_name

    def logical_delete(self):
        """逻辑删除奖项"""
        try:
            with transaction.atomic():
                self.is_deleted = True
                self.save()
        except Exception:
            return False
        else:
            return True


class ApplicationManager(models.Manager):
    """申请管理类"""

    def all(self):
        """重载all"""
        return super(models.Manager, self).filter(is_deleted=False)

    def awarded(self, username):
        """根据username查询已过期的奖项"""
        try:
            qq = User.objects.get(username=username).get_qq()
        except ObjectDoesNotExist, err:
            print err
            return []
        apps = Application.objects.all().filter(status=4, award__organization__applicant__contains=qq)
        data = apps.values('key', 'award__organization__name', 'award__name', 'created_time', 'applicant')
        data = json.dumps(list(data), cls=DateJSONEncoder)
        data = json.loads(data)
        return data

class Application(models.Model):
    """奖项申请"""
    applicant = models.CharField(max_length=30, verbose_name=u'申请人/团队')
    introduction = models.TextField(verbose_name=u'事迹介绍')

    STATUS_CHOICES = (
        (0, u'未审核'),
        (1, u'未通过'),
        (2, u'已通过'),
        (3, u'未获奖'),
        (4, u'已获奖')
    )
    # 获取状态码对应的字符串的方法： Model.get_FOO_display(), (FOO: 字段名字)
    status = models.IntegerField(verbose_name=u'申请状态', choices=STATUS_CHOICES)
    award = models.ForeignKey(to=Award, verbose_name=u'奖项', on_delete=models.CASCADE)
    created_time = models.DateTimeField(verbose_name=u'创建时间', auto_now_add=True)
    is_deleted = models.BooleanField(verbose_name=u'逻辑删除', default=False)
    key = models.CharField(max_length=64, verbose_name=u'申报标识', unique=True)

    objects = ApplicationManager()

    class Mate:
        verbose_name = u'奖项申请'
        verbose_name_plural = verbose_name

    def logical_delete(self):
        """逻辑删除申请"""
        try:
            with transaction.atomic():
                self.is_deleted = True
                self.save()
        except Exception:
            return False
        else:
            return True


class Accessory(models.Model):
    """
    附件
    name: 附件名字，唯一，不可重复
    """
    key = models.CharField(max_length=64, verbose_name=u'附件标志', unique=True)
    name = models.CharField(max_length=128, verbose_name=u'附件名称')
    path = models.CharField(max_length=128, verbose_name=u'附件路径')
    application = models.ForeignKey(to=Application, verbose_name=u'奖项申报', on_delete=models.CASCADE)

    class Mate:
        verbose_name = u'附件'
        verbose_name_plural = verbose_name


class Review(models.Model):
    """申请评审"""
    comment = models.TextField(verbose_name=u'评语', blank=True)
    application = models.ForeignKey(to=Application, verbose_name=u'奖项申报', on_delete=models.CASCADE)
    is_pass = models.BooleanField(verbose_name=u'是否通过', default=False)
    is_awarded = models.BooleanField(verbose_name=u'是否获奖', default=False)

    class Mate:
        verbose_name = u'申请评价'
        verbose_name_plural = verbose_name
