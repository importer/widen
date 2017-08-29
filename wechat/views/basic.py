# -*- coding: utf-8 -*-
from django.http import HttpResponseBadRequest, HttpResponse
from django.shortcuts import render
import logging, json
from wechat.api_errors import *
from wechat.models.basic import *
from wechat.models import basic, wechat_info
from django.views.decorators.csrf import csrf_exempt
from wechat.utils.utils import *
from wechat.utils.sign import Sign
from widen import settings

from wechat.models import templatesend
from wechat_sdk import WechatConf
from wechat_sdk import WechatBasic
from wechat_sdk.exceptions import ParseError
from wechat_sdk.messages import (TextMessage, VoiceMessage, ImageMessage, VideoMessage, LinkMessage, LocationMessage,
                                 EventMessage, ShortVideoMessage)
from wechat.views.response import ResponseFun

conf = WechatConf(
    token=settings.WX_TOKEN,
    appid=settings.APP_ID,
    appsecret=settings.APP_SECRET,
    encrypt_mode='YOUR_MODE',
    encoding_aes_key='YOUR_AES_KEY'
)

# Create your views here.

wechat_instance = WechatBasic(conf=conf)


@csrf_exempt
def index(request):
    signature = request.GET.get('signature')
    # print request.GET
    timestamp = request.GET.get('timestamp')
    nonce = request.GET.get('nonce')
    # print wechat_instance.get_access_token()
    if not wechat_instance.check_signature(signature=signature, timestamp=timestamp, nonce=nonce):
        return HttpResponseBadRequest('Verify Failed')
    else:
        if request.method == 'GET':
            response = request.GET.get('echostr', 'error')
        else:
            try:
                wechat_instance.parse_data(request.body)
                message = wechat_instance.get_message()
                reply_text=''
                if isinstance(message, TextMessage):
                    reply_text = ResponseFun['TextMessage'](message, wechat_instance)
                elif isinstance(message, VoiceMessage):
                    reply_text = ResponseFun['VoiceMessage'](message)
                elif isinstance(message, ImageMessage):
                    reply_text = ResponseFun['ImageMessage'](message)
                elif isinstance(message, LinkMessage):
                    reply_text = ResponseFun['LinkMessage'](message)
                elif isinstance(message, LocationMessage):
                    reply_text = ResponseFun['LocationMessage'](message)
                elif isinstance(message, VideoMessage):
                    reply_text = ResponseFun['VideoMessage'](message)
                elif isinstance(message, ShortVideoMessage):
                    reply_text = ResponseFun['ShortVideoMessage'](message)
                elif isinstance(message, EventMessage):
                    reply_text = ResponseFun['EventMessage'](message, wechat_instance)
                    return HttpResponse(reply_text,
                                        content_type="application/xml")
                response = wechat_instance.response_text(content=reply_text)
            except ParseError:
                return HttpResponseBadRequest('Invalid XML Data')
        return HttpResponse(response, content_type="application/xml")


def send_template(request):
    if request.method == 'POST':
        data = request.POST
        wechat_instance.send_template_message(data)
        return HttpResponse('success')
    openid = request.GET.get('openid')
    # url=request.GET.get('url')
    id = request.GET.get('msid')
    tid = request.GET.get('tmpid')
    temp_data = templatesend.SendMessage.objects.get(pk=id)
    tid_date = templatesend.TemplateidInfo.objects.get(pk=tid)
    data = tid_date.template_desc % (temp_data.title,
                                     temp_data.author,
                                     temp_data.publish,
                                     temp_data.description,
                                     temp_data.status
                                     )
    url = temp_data.url
    # print data
    data = json.loads(data)
    print (url)
    wechat_instance.send_template_message(openid, tid_date.template_id, data, url)
    return HttpResponse('success')


def get_access_token_view(request):
    new_token = basic.AccessToken.objects.all()
    token = new_token.accesstoken
    logging.info(token)
    context_data = {
        'access_token': token,
    }
    return render(request, 'get_access_token.html', context_data)


def admin_dashboard(request):
    access_token_url = settings.APP_URL + "wechat/tokenget/"
    qr_code_ticket = settings.APP_URL + "wechat/showticket/"
    wechat_infos = wechat_info.WechatUser.objects.all()[0]
    openid = wechat_infos.openid
    u_id = wechat_infos.id
    Tinfo = templatesend.TemplateidInfo.objects.get(pk=2)
    tid = Tinfo.id
    context_data = {
        "access_token_url": access_token_url,
        "qr_code_ticket": qr_code_ticket,
        "template_url": 'http://localhost/wechat/send_template?openid=%s&msid=%s&tmpid=%s' % (openid, u_id, tid)
    }
    return render(request, 'admin-dashboard.html', context_data)


def get_qr_code_ticket(request):
    from wechat.utils.utils import get_temp_qr_code, get_pergmanent_qr_code
    temp_url = get_temp_qr_code()
    pergmanent_url = get_pergmanent_qr_code()
    context_data = {
        'temp': temp_url,
        'permanent': pergmanent_url
    }
    return render(request, 'ticket.html', context_data)


def weixin_web(request):
    jsapi_ticket = wechat_instance.get_jsapi_ticket()
    now_url = 'http://' + request.get_host() + request.get_full_path()
    sign = Sign(jsapi_ticket.get('jsapi_ticket'), now_url)
    sign_key = sign.sign()
    return render(request, 'wechat_demo.html', {'sign_key': sign_key})
