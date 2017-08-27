# coding=utf-8
from django.db import models
from wechat.models.wechat_info import WechatUser
import datetime


# from django.contrib.auth.models import User


class SendMessage(models.Model):
    STATUS_CHOICES = (
        ('0', 'Wait'),
        ('1', 'Published'),
        ('2', 'Success')
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
    publish = models.DateField(default='')
    # 模板ID
    template_id = models.CharField(max_length=250)
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


class SendToUser(models.Model):
    """docstring for User"""
    STATUS_CHOICES = (
        ('0', 'Ready'),
        ('1', 'Send'),
        ('3', 'Success'),
        ('4', 'Fail'),
    )
    message_id = models.CharField(max_length=100)
    openid = models.SlugField(max_length=250)
    group_id = models.SlugField(max_length=250)
    plan_date = models.DateTimeField(auto_now_add=True)
    send_time = models.DateTimeField(auto_now_add=True)
    mask = models.TextField()
    status = models.CharField(max_length=10,
                              choices=STATUS_CHOICES, default='0')

    def __unicode__(self):
        return self.user_name


class TemplateidInfo(models.Model):
    template_id = models.CharField(max_length=100)
    template_desc = models.TextField()

    def __unicode__(self):
        return self.template_desc


class addinfo(models.Model):
    url = models.CharField(max_length=500)
    title = models.CharField(max_length=2000)
    add_datetime = models.DateTimeField(auto_now=True)
    user_id = models.CharField(max_length=200)
    order_id = models.IntegerField()

    def __unicode__(self):
        return self.title
