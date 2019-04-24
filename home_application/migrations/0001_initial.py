# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Applicant',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('applied', models.CharField(max_length=60, verbose_name='\u5df2\u7ecf\u7533\u8bf7\u7684\u5956\u9879')),
                ('statu', models.CharField(max_length=60, verbose_name='\u5ba1\u6279\u72b6\u6001')),
            ],
        ),
        migrations.CreateModel(
            name='ApplicationRecord',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('applicant', models.ForeignKey(to='home_application.Applicant', blank=True)),
            ],
            options={
                'verbose_name': '\u5956\u9879\u7533\u8bf7\u8bb0\u5f55',
            },
        ),
        migrations.CreateModel(
            name='Award',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('awardName', models.CharField(max_length=60, verbose_name='\u5956\u9879\u540d\u79f0')),
                ('conditions', models.TextField(verbose_name='\u7533\u8bf7\u6761\u4ef6')),
                ('level', models.CharField(max_length=60, verbose_name='\u5956\u9879\u7ea7\u522b')),
                ('awardStatu', models.BooleanField(default=False, verbose_name='\u6240\u6709\u7684\u5956\u9879\u7684\u72b6\u6001\uff08\u662f\u5426\u53ef\u7533\u8bf7\uff09')),
            ],
            options={
                'verbose_name': '\u5956\u9879\u4fe1\u606f',
            },
        ),
        migrations.CreateModel(
            name='CanApply',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('awardName', models.CharField(max_length=60, verbose_name='\u53ef\u7533\u8bf7\u7684\u5956\u9879\u540d\u79f0')),
            ],
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('memName', models.CharField(max_length=60, verbose_name='\u961f\u5458\u59d3\u540d')),
            ],
        ),
        migrations.CreateModel(
            name='My',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('myOrg', models.CharField(max_length=60, verbose_name='\u6240\u5c5e\u7ec4\u7ec7')),
                ('myText', models.TextField(verbose_name='\u6211\u7684\u6587\u6863')),
                ('myApplied', models.CharField(max_length=60, verbose_name='\u5df2\u7533\u8bf7\u7684\u5956\u9879')),
                ('myStatus', models.CharField(max_length=60, verbose_name='\u7533\u8bf7\u7684\u5956\u9879\u7684\u72b6\u6001')),
                ('myAward', models.CharField(max_length=60, verbose_name='\u5df2\u83b7\u5f97\u7684\u5956\u9879')),
            ],
            options={
                'verbose_name': '\u6211\u7684\u5956\u9879',
            },
        ),
        migrations.CreateModel(
            name='MyFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fileName', models.CharField(max_length=60, verbose_name='\u6587\u4ef6\u540d')),
                ('filePath', models.FilePathField(verbose_name='\u6587\u4ef6\u8def\u5f84')),
            ],
            options={
                'verbose_name': '\u6211\u7684\u6587\u4ef6',
            },
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('orgID', models.IntegerField(max_length=60, verbose_name='\u7ec4\u7ec7ID')),
                ('orgName', models.CharField(max_length=60, verbose_name='\u7ec4\u7ec7\u540d\u79f0')),
                ('leader', models.CharField(max_length=60, verbose_name='\u7ec4\u7ec7\u8d1f\u8d23\u4eba')),
                ('updateUser', models.CharField(max_length=60, verbose_name='\u64cd\u4f5c\u8005')),
                ('lastTime', models.DateTimeField(verbose_name='\u64cd\u4f5c\u65f6\u95f4')),
                ('member', models.ForeignKey(to='home_application.Member', blank=True)),
            ],
            options={
                'verbose_name': '\u7ec4\u7ec7\u4fe1\u606f',
            },
        ),
        migrations.AddField(
            model_name='my',
            name='myFile',
            field=models.ForeignKey(to='home_application.MyFile', blank=True),
        ),
        migrations.AddField(
            model_name='award',
            name='org',
            field=models.ForeignKey(to='home_application.Organization'),
        ),
        migrations.AddField(
            model_name='applicationrecord',
            name='canApply',
            field=models.ForeignKey(to='home_application.CanApply', blank=True),
        ),
    ]
