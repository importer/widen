# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Post,User,Wxuser,Token


#published action
def make_published(modeladmin, request, queryset):  
    queryset.update(status='published')  
    modeladmin.message_user(request, "%s successfully updated." % queryset.count())  
make_published.short_description = "message published"  
# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title','author','url','description','model_id','group_id','publish','status',)
    actions=['make_published']
    ordering = ['publish']

@admin.register(Wxuser)
class WxUser(admin.ModelAdmin):
    list_display = ('openid','nickname','sex','headimgurl','privilege')

@admin.register(Token)
class Token(admin.ModelAdmin):
    list_display = ('access_token', 'expires_in', 'refresh_token', 'openid', 'scope')

admin.site.register(User)
# admin.site.register(kombu_models.Message)