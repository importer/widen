# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Register your models here.
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from wechat.models import basic
from wechat.models import wechat_menu
from wechat.models import wechat_info
from wechat.models import wechat_server
from wechat.models import templatesend
import datetime
from django import forms


@admin.register(basic.LocationEvent)
class LocationEventAdmin(admin.ModelAdmin):
    list_display = ('latitude', 'longitude', 'precision',)


@admin.register(basic.TextMessage)
class TextMessage(admin.ModelAdmin):
    list_display = ('message_id', 'create_time', 'from_user_name', 'message_content',)


@admin.register(basic.MenuEvent)
class MenuMessage(admin.ModelAdmin):
    list_display = ('message_type', 'create_time', 'from_user_name', 'event', 'event_key',)


@admin.register(basic.LocationMessage)
class LocationMessage(admin.ModelAdmin):
    list_display = ('label', 'create_time', 'from_user_name', 'location_x', 'location_y', 'scale')


@admin.register(basic.MessageAutoReplay)
class MessageAutoReplay(admin.ModelAdmin):
    list_display = ('content', 'create_time', 'rule',)


@admin.register(basic.PicMessage)
class PicMessage(admin.ModelAdmin):
    list_display = ('message_id', 'create_time', 'from_user_name', 'pic_url', 'media_id')


@admin.register(basic.TemplateEvent)
class TemplateMessage(admin.ModelAdmin):
    list_display = ('msgid', 'create_time', 'status',)


@admin.register(wechat_info.WechatUser)
class WechatUserInfo(admin.ModelAdmin):
    list_display = ('openid', 'nickname', 'sex', 'city', 'remark',)


@admin.register(templatesend.SendToUser)
class SendToUser(admin.ModelAdmin):
    list_display = ('message_id', 'openid', 'group_id', 'plan_date', 'mask', 'status',)


@admin.register(templatesend.TemplateidInfo)
class TemplateidInfo(admin.ModelAdmin):
    list_display = ('template_id', 'template_desc',)


def intomessage(modeladmin, request, queryset):
    results = queryset.all().order_by('order_id')
    querysetlist = []
    start_time = datetime.datetime.now()
    for result in results:
        SendMessage = templatesend.SendMessage
        publish = (start_time + datetime.timedelta(days=result.order_id)).strftime("%Y-%m-%d")
        # print result.title,result.url,result.order_id,publish
        querysetlist.append(SendMessage(title=result.title,
                                        author='@bigbigzzw',
                                        url=result.url,
                                        description=result.title,
                                        publish=publish,
                                        template_id='NhAjvkKejw9ZFACNCjQCFNhsrsui0tKA5HGl7HetWZQ',
                                        status=0))
    SendMessage.objects.bulk_create(querysetlist)
    modeladmin.message_user(request, "%s successfully updated." % queryset.count())


intomessage.short_description = "更新消息"


@admin.register(templatesend.addinfo)
class addinfo(admin.ModelAdmin):
    list_display = ('title', 'url', 'add_datetime', 'user_id', 'order_id')
    search_fields = ('title',)
    list_per_page = 15
    list_filter = ('order_id',)
    date_hierarchy = 'add_datetime'
    ordering = ('add_datetime',)
    actions = [intomessage]


class data_src_form(forms.forms.Form):
        _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
        # data_src = forms.CharField()
        data_src = forms.ModelChoiceField(wechat_info.WechatUser.objects.all())

def update_data_src(modeladmin, request, queryset):
    form = None
    if 'cancel' in request.POST:
        modeladmin.message_user(request, u'已取消')
        return
    elif 'data_src' in request.POST:
        form = data_src_form(request.POST)
        if form.is_valid():
            data_src = form.cleaned_data['data_src']
            openid= data_src.openid
            for case in queryset:
                case.author = openid
                case.save()
            modeladmin.message_user(request, "%s successfully updated." % queryset.count())
            return HttpResponseRedirect(request.get_full_path())
        else:
            modeladmin.message_user(request, u"请选择推送用户")
            form = None

    if not form:
        form = data_src_form(initial={'_selected_action': request.POST.getlist(admin.ACTION_CHECKBOX_NAME)})
    return render_to_response('batch_update.html',
                              {'objs': queryset, 'form': form, 'path': request.get_full_path(),
                               'action': 'update_data_src', 'title': u'批量更改/选择推送用户'},
                              context_instance=RequestContext(request)
                              )


update_data_src.short_description = u'批量修改、选择推送用户'


@admin.register(templatesend.SendMessage)
class SendMessage(admin.ModelAdmin):
    list_display = ('title', 'author', 'description', 'publish', 'template_id', 'status',)
    actions = [update_data_src]


admin.site.register(wechat_menu.TopLevelMenu)
admin.site.register(wechat_server.WeChatServer)
admin.site.register(wechat_info.WechatOpenid)
# admin.site.register(wechat_info.WechatUser)
