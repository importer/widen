# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


# Create your models here.
class Post(models.Model):
    STATUS_CHOICES = (
        ('wait', 'Wait'),
        ('published', 'Published'),
        ('success', 'Success')
    )
    # 标题内容
    title = models.CharField(max_length=250)
    # 作者
    author = models.CharField(max_length=250)
    # 访问的url
    url = models.CharField(max_length=250)
    # 内容
    description = models.TextField()
    # 推送时间
    publish = models.DateTimeField()
    # 模板ID
    model_id = models.CharField(max_length=250)
    # 推送用户组ID
    group_id = models.CharField(max_length=250)
    # 创建时间
    created = models.DateTimeField(auto_now_add=True)
    # 更新时间
    updated = models.DateTimeField(auto_now=True)
    # 状态
    status = models.CharField(max_length=10,
                              choices=STATUS_CHOICES, default='wait')

    class Meta:
        ordering = ('-publish',)

    def __unicode__(self):
        return self.title


class User(models.Model):
    """docstring for User"""
    STATUS_CHOICES = (
        ('register', 'Register'),
        ('alive', 'Alive'),
        ('bealive', 'Bealive'),
        ('black', 'Black'),
    )
    user_id = models.SlugField(max_length=250)
    add_time = models.DateTimeField(auto_now_add=True)
    user_name = models.CharField(max_length=250)
    content = models.TextField()
    status = models.CharField(max_length=10,
                              choices=STATUS_CHOICES, default='bealive')

    def __unicode__(self):
        return self.user_name

class Token(models.Model):
    access_token=models.CharField(max_length=100)
    expires_in=models.IntegerField()
    refresh_token=models.CharField(max_length=100)
    openid=models.CharField(max_length=100)
    scope=models.CharField(max_length=100)

    def __unicode__(self):
        return self.openid

class Wxuser(models.Model):
    openid = models.CharField(max_length=50)
    nickname = models.CharField(max_length=50)
    sex = models.CharField(max_length=2)
    province = models.CharField(max_length=10)
    city = models.CharField(max_length=20)
    country = models.CharField(max_length=20)
    headimgurl = models.CharField(max_length=100)
    privilege = models.CharField(max_length=50)
    unionid = models.CharField(max_length=50)
    language = models.CharField(max_length=50)

    def __unicode__(self):
        return self.openid

class UserSubmit(models.Model):
    title=models.CharField(max_length=200,verbose_name='标题')
    url=models.URLField(verbose_name='URL')
    plandate=models.DateField(verbose_name='推送日期')
    rule=models.CharField(max_length=50,verbose_name='提取规则')
    description=models.TextField(max_length=400,verbose_name='描述')
    select_user=models.CharField(max_length=40,verbose_name='推送方式',choices=(('1','微信'),('2','邮箱'),('0','模版消息'),))
    def __unicode__(self):
        return self.title