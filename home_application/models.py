# -*- coding: utf-8 -*-

# import from apps here


# import from lib

from django.db import models

class CanApply(models.Model):
    awardName = models.CharField(max_length=60, verbose_name=u'可申请的奖项名称')
    def __str__(self):
        return self.awardName

class Applicant(models.Model):
    applied = models.CharField(max_length=60, verbose_name=u'已经申请的奖项')
    statu = models.CharField(max_length=60, verbose_name=u'审批状态')

class ApplicationRecord(models.Model):
    applicant = models.ForeignKey(Applicant,blank=True)
    canApply = models.ForeignKey(CanApply, blank=True)

    class Meta:
        verbose_name = u'奖项申请记录'

class Member(models.Model):
    memName = models.CharField(max_length=60,verbose_name=u'队员姓名')

class Organization(models.Model):
    orgID = models.IntegerField(max_length=60, verbose_name=u'组织ID')
    orgName = models.CharField(max_length=60, verbose_name=u'组织名称' )
    leader = models.CharField(max_length=60, verbose_name=u'组织负责人' )
    updateUser = models.CharField(max_length=60, verbose_name=u'操作者' )
    lastTime = models.DateTimeField(verbose_name=u'操作时间')
    member = models.ForeignKey(Member, blank=True)

    class Meta:
        verbose_name = u'组织信息'

class Award(models.Model):
    awardName = models.CharField(max_length=60, verbose_name=u'奖项名称' )
    conditions = models.TextField(verbose_name=u'申请条件')
    level = models.CharField(max_length=60, verbose_name=u'奖项级别')
    org = models.ForeignKey(Organization,blank=False)
    awardStatu = models.BooleanField(verbose_name=u'所有的奖项的状态（是否可申请）', default=False)

    class Meta:
        verbose_name = u'奖项信息'

class MyFile(models.Model):
    fileName = models.CharField(max_length=60, verbose_name=u'文件名')
    filePath = models.FilePathField(verbose_name=u'文件路径')

    class Meta:
        verbose_name = u'我的文件'

class My(models.Model):
    myOrg = models.CharField(max_length=60,verbose_name=u'所属组织')
    myText = models.TextField(verbose_name=u'我的文档')
    myApplied = models.CharField(max_length=60, verbose_name=u'已申请的奖项')
    myStatus = models.CharField(max_length=60, verbose_name=u'申请的奖项的状态')
    myAward = models.CharField(max_length=60, verbose_name=u'已获得的奖项')
    myFile = models.ForeignKey(MyFile,blank=True)

    class Meta:
        verbose_name = u'我的奖项'


