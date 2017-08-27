# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
# from index.tasks import add, send
import requests
import logging
import json

from django.views.generic import ListView
from django.views.generic import DetailView
from index.utils.webuserinfo import WeiXinLogin
from index.models import Wxuser, UserSubmit
from index.form import Usersubmit
from widens import settings
from wechat.models.templatesend import addinfo
from wechat.models.basic import TextMessage

logger = logging.getLogger('django')


def index(request):
    # del request.session['openid']
    REDIRECT_URL = settings.REDIRECT_URL
    if request.session.get('openid', False):
        logger.info('直接获取[opendi]' + request.session.get('openid', False))
        # print request.session.get('openid', False)
        WxDetaile = Wxuser.objects.filter(openid=request.session.get('openid', False))[0]
        re_detail = {'city': WxDetaile.city.encode('utf-8'),
                     'country': WxDetaile.country.encode('utf-8'),
                     'nickname': WxDetaile.nickname.encode('utf-8'),
                     'sex': WxDetaile.sex.encode('utf-8'),
                     'headimgurl': WxDetaile.headimgurl.encode('utf-8')}
        # print WxDetaile.country
        # return HttpResponse(WxDetaile)
        return render(request, 'UserInfo.html', {'WxDetaile': WxDetaile})
    if request.GET.get("code") == None:
        return HttpResponseRedirect(REDIRECT_URL)
    # 第一步获取code跟state
    code = request.GET.get("code")
    state = request.GET.get("state")
    logger.info('获取用户信息[code]' + code + '[state]' + state)
    wx = WeiXinLogin(code, state)
    UserDetaile = wx.get_detail()
    request.session['openid'] = UserDetaile.get('openid')
    # print UserDetaile
    re_UserDetaile = {'city': UserDetaile.get('city').encode('iso8859-1').decode('utf-8'),
                      'country': UserDetaile.get('country').encode('iso8859-1').decode('utf-8'),
                      'nickname': UserDetaile.get('nickname').encode('iso8859-1').decode('utf-8'),
                      'sex': UserDetaile.get('sex').encode('iso8859-1').decode('utf-8'),
                      'headimgurl': UserDetaile.get('headimgurl').encode('iso8859-1').decode('utf-8')}
    # return HttpResponse(json.dumps(re_UserDetaile))
    return render(request, 'UserInfo.html', {'WxDetaile': re_UserDetaile})


def weui(request):
    if request.method == "POST":
        message = TextMessage.objects.all().order_by('-create_time')[0]
        return HttpResponse(message.message_content)
    return render(request, 'danmu.html')


def register(request):
    return render(request, 'register.html')


def userinfo(request):
    return render(request, 'UserInfo.html')


def base(request):
    return render(request, 'w_base.html')


# @login_required
def get_detail(request):
    details = UserSubmit.objects.all().order_by('-plandate')[:5]
    # print details.title
    return render(request, 'DetailList.html', {'details': details})


class InfoDetail(DetailView):
    model = addinfo
    context_object_name = 'detail'
    template_name = 'Detail.html'


class InfoListView(ListView):
    model = addinfo
    template_name = 'DetailList.html'
    paginate_by = 10

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        self.user_id = request.user.id
        return super(InfoListView, self).get(request, *args, **kwargs)

    def get_queryset(self):
        return addinfo.objects.filter(user_id=self.user_id).order_by('add_datetime')

    def get_context_data(self, **kwargs):
        context = super(InfoListView, self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context


def uploader(request):
    return render(request, 'uploader.html')


def test(request):
    return render(request, 'add.html')


# @login_required
@csrf_exempt
def addUserSubmit(request):
    if request.method == 'POST':
        form = Usersubmit(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return HttpResponse('success')
        else:
            # return render(request,'error.html',{'form':form})
            return HttpResponse('fail')
    else:
        form = Usersubmit()
        return render(request, 'add.html', {'form': form})


def get_info(request):
    if request.session.get('openid', False):
        print request.session.get('openid', False)
        WxDetaile = Wxuser.objects.get(openid=request.session.get('openid', False))
        re_detail = {'city': WxDetaile.city.encode('utf-8'),
                     'country': WxDetaile.country.encode('utf-8'),
                     'country': WxDetaile.nickname.encode('utf-8'),
                     'sex': WxDetaile.sex.encode('utf-8'),
                     'headimgurl': WxDetaile.headimgurl.encode('utf-8')}
        return HttpResponse(json.dumps(re_detail))
    # 第一步获取code跟state
    # try:
    if request.GET.get("code") == None:
        return HttpResponseRedirect()
    code = request.GET.get("code")
    state = request.GET.get("state")
    logging.info('code:' + code + ';state:' + state)
    wx = WeiXinLogin(code, state)
    UserDetaile = wx.get_detail()
    request.session['openid'] = UserDetaile.get('openid')
    print UserDetaile
    html = '<html><body><img src="%s"  alt="%s" />%s </body></html>' % (
        UserDetaile.get('headimgurl'), UserDetaile.get('openid'), UserDetaile.get('nickname'))
    return HttpResponse(html)
