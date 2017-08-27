from django.db import models
from django.conf import settings


class WechatUser(models.Model):
    subscribe = models.CharField(default="", max_length=20)
    openid = models.CharField(default="", max_length=20,unique=True)
    nickname = models.CharField(default="", max_length=200)
    sex = models.CharField(default="", max_length=20)
    city = models.CharField(default="", max_length=40)
    country = models.CharField(default="", max_length=40)
    province = models.CharField(default="", max_length=40)
    language = models.CharField(default="", max_length=20)
    headimgurl = models.CharField(default="", max_length=100)
    subscribe_time = models.CharField(default="", max_length=50)
    unionid = models.CharField(default="", max_length=40)
    remark = models.CharField(default="", max_length=100)
    groupid = models.CharField(default="", max_length=20)

    def __unicode__(self):
        return self.openid


class WechatOpenid(models.Model):
    openid = models.CharField(default='', max_length=40)

    def __unicode__(self):
        return self.openid
