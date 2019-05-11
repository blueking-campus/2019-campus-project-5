# -*- coding: utf-8 -*-
import json
import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models import Q
from django.db import transaction
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger

from home_application.utils import (
    DateJSONEncoder, generateUUID
)
class UserManager(models.Manager):
    """用户管理"""
    def username_exist(self, username):
        """username是否存在"""
        try:
            super(models.Manager, self).get(username=username)
            return True
        except ObjectDoesNotExist, err:
            print err
            return False


    def qq_exist(self, qq):
        """qq是否存在"""
        try:
            super(models.Manager, self).get(qq=qq)
            return True
        except ObjectDoesNotExist, err:
            print err
            return False

class User(models.Model):
    """用户关联表"""
    username = models.CharField(max_length=64, verbose_name=u'用户名', unique=True)
    qq = models.CharField(max_length=64, verbose_name=u'qq号码', unique=True)

    objects = UserManager()

    class Mate:
        verbose_name = u'用户关联'
        verbose_name_plural = verbose_name

    def get_qq(self):
        """获取qq"""
        return self.qq

    def save_qq(self, username, qq):
        try:
            with transaction.atomic():
                self.username = username
                self.qq = qq
                self.save()
        except Exception, err:
            # 数据库操作失败，创建组织失败
            print err
            return False
        else:
            # 创建组织成功
            return True

class LevelManager(models.Manager):
    """级别管理类"""
    def all_list(self):
        return super(models.Manager, self).all().values_list('name', flat=True)

class Level(models.Model):
    """奖项级别"""
    name = models.CharField(max_length=64, verbose_name=u'级别', unique=True)
    objects = LevelManager()

    class Mate:
        verbose_name = u'级别'
        verbose_name_plural = verbose_name

    def __unicode__(self):
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

    def all_name_key(self):
        """查询所有未逻辑删除的组织 只返回名字和key"""
        orgs = super(models.Manager, self).filter(is_deleted=False)
        # 格式化数据
        data = orgs.values('key', 'name')
        return data




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

    def __unicode__(self):
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
        except Exception, err:
            print 'Organization:updata update error:', err
            return False
        else:
            return True


class AwardManager(models.Manager):
    """奖项管理类"""

    def all(self, name, organization, status, date_time, page=1, page_size=10):
        """查询所有未逻辑删除的奖项"""

        # 所有未逻辑删除的奖项
        awards = super(models.Manager, self).filter(is_deleted=False)

        if name:
            # 模糊查询奖项名
            awards = awards.filter(name__icontains=name)
        if organization:
            # 模糊查询组织名
            awards = awards.filter(organization__name__icontains=organization)
        if status == 1:
            # 查询奖项状态
            # status: (0, 不限)， (1, 过期), (2, 生效)
            now = datetime.datetime.now()
            awards = awards.filter(Q(begin_time__gte=now) | Q(end_time__lte=now) | Q(is_active=False))
        elif status == 2:
            now = datetime.datetime.now()
            awards = awards.filter(begin_time__lte=now, end_time__gte=now, is_active=True)
        if date_time:
            # 查询时间
            date_time = datetime.datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S")
            awards = awards.filter(begin_time__lte=date_time, end_time__gte=date_time)

        # 分页
        response = {}
        paginator = Paginator(awards, page_size)
        response['recordsTotal'] = paginator.count
        response['recordsFiltered'] = paginator.count

        print response
        try:
            awards = paginator.page(page).object_list
        except PageNotAnInteger:
            awards = paginator.page(1).object_list
        except EmptyPage:
            awards = paginator.page(paginator.num_pages).object_list
        except ZeroDivisionError:
            response['awards'] = []
            return response

        # 格式化数据
        # awards.extra(select={'status': "IF(is_active, '生效中', '已过期')"})
        data = awards.values('key', 'name', 'requirement', 'level__name',
                             'organization__name', 'is_active', 'begin_time', 'is_attached',
                             'end_time', 'apply_number', 'awarded_number')
        data = json.dumps(list(data), cls=DateJSONEncoder)
        data = json.loads(data)
        response['data'] = data
        return response

    def all_by_username(self, username, is_active=True):
        """通过username查询该username可参加的奖项"""
        try:
            qq = User.objects.get(username=username).get_qq()
        except ObjectDoesNotExist, err:
            print 'AwardManager:all_by_username: get qq by username:', err
            return []
        awards = super(models.Manager, self).filter(is_deleted=False)
        if is_active:
            now = datetime.datetime.now()
            awards = awards.filter(begin_time__lte=now, end_time__gte=now, is_active=is_active)
        else:
            now = datetime.datetime.now()
            awards = awards.filter(Q(begin_time__gte=now) | Q(end_time__lte=now) | Q(is_active=is_active))
        # 格式化数据
        # awards.extra(select={'status': "if is_active '生效中' else '已过期')"})
        data = awards.values('key', 'name', 'requirement', 'level__name',
                             'organization__name', 'is_active', 'begin_time', 'is_attached',
                             'end_time', 'apply_number', 'awarded_number')
        data = json.dumps(list(data), cls=DateJSONEncoder)
        data = json.loads(data)
        return data

    def get_values(self, key):
        """根据key返回对应的award的dirc格式数据"""
        try:
            award = super(models.Manager, self).get(key=key)
            data = {
                'key': award.key,
                'name': award.name,
                'requirement': award.requirement,
                'level__name': award.level.name,
                'organization__key': award.organization.key,
                'is_active': award.is_active,
                'begin_time': award.begin_time,
                'is_attached': award.is_attached,
                'end_time': award.end_time,
                'apply_number': award.apply_number,
                'awarded_number': award.awarded_number
            }
        except ObjectDoesNotExist, err:
            print 'AwardManager:get_values award not exist', err
            raise ObjectDoesNotExist('AwardManager:get_values award not exist:', err)
        else:
            return data



    def delete(self, key_list):
        """批量逻辑删除奖项"""
        try:
            with transaction.atomic():
                super(models.Manager, self).filter(key__in=key_list).updata(is_deleted=True)
        except Exception, err:
            print 'Award:delete update error:', err
            return False
        else:
            return True



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

    @classmethod
    def create(cls, data, *args, **kwargs):
        """创建奖项"""
        name = data.get('name')
        requirement = data.get('requirement')
        level__name = data.get('level__name')
        organization__key = data.get('organization__key')
        begin_time = data.get('begin_time')
        end_time = data.get('end_time')
        is_attached = data.get('is_attached')
        is_active = data.get('is_active')

        print level__name, type(level__name)
        try:
            level = Level.objects.get(name=level__name)
            organization = Organization.objects.get(key=organization__key)
        except ObjectDoesNotExist, err:
            raise ObjectDoesNotExist('Award:create get level and organization error:', err)

        try:
            with transaction.atomic():
                award = cls()
                award.name = name
                award.requirement = requirement
                award.level = level
                award.organization = organization
                award.begin_time = begin_time
                award.end_time = end_time
                award.is_active = is_active
                award.is_attached = is_attached
                award.key = generateUUID()
                award.is_deleted = False
                award.awarded_number = 0
                award.apply_number = 0
                award.save()
        except ValueError, err:
            print 'Award:create save models err:', err
            raise ValueError('Award:create save models err:', err)
        else:
            return True

    @classmethod
    def change(cls, data, *args, **kwargs):
        """修改奖项"""
        key = data.get('key')
        name = data.get('name')
        requirement = data.get('requirement')
        level__name = data.get('level__name')
        organization__key = data.get('organization__key')
        begin_time = data.get('begin_time')
        end_time = data.get('end_time')
        is_attached = data.get('is_attached')
        is_active = data.get('is_active')
        try:
            level = Level.objects.get(name=level__name)
            organization = Organization.objects.get(key=organization__key)
        except ObjectDoesNotExist, err:
            raise ObjectDoesNotExist('Award:change get level and organization error:', err)
        try:
            award = cls.objects.get(key=key)
            award.name = name
            award.requirement = requirement
            award.level = level
            award.organization = organization
            award.begin_time = begin_time
            award.end_time = end_time
            award.is_active = is_active
            award.is_attached = is_attached
            award.save()
        except ObjectDoesNotExist, err:
            print 'Award:change award key not exist:', err
            raise ObjectDoesNotExist('Award:change award key not exist:', err)
        except ValueError, err:
            print 'Award:change error in save award:', err
            raise ValueError('Award:change error in save award:', err)
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
            print 'ApplicationManager:awarded get qq by username:', err
            return []
        now = datetime.datetime.now()
        apps = Application.objects.all().filter(award__organization__applicant__contains=qq, status=4)
        apps = apps.filter(Q(award__begin_time__gte=now) | Q(award__end_time__lte=now) | Q(award__is_active=False))

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
