# coding=utf-8
from wechat.models import basic, wechat_info
from wechat.models.wechat_info import WechatUser, WechatOpenid
from wechat.models import templatesend
from django.http import HttpResponseBadRequest, HttpResponse

def TextResponse(message,wechat_instance):
    Textmessage = basic.TextMessage(to_user_name=message.target,
                                    from_user_name=message.source,
                                    create_time=message.time,
                                    message_type=message.type,
                                    message_id=message.id,
                                    message_content=message.content)
    Textmessage.save()
    if message.content == u'send_template':
        return 'send_template()'
    elif message.content == u'get_user':
        ADD = []
        Openid_list = wechat_instance.get_followers(first_user_id=None)
        ADD = [WechatOpenid(openid=i) for i in Openid_list['data']['openid']]
        WechatOpenid.objects.bulk_create(ADD)
        openid = WechatOpenid.objects.all()[:100]
        for id in openid:
            Wechat_user = wechat_instance.get_user_info(id, lang='zh_CN')
            Wechat_user.pop('tagid_list')
            Wechat_User = WechatUser(**Wechat_user)
            Wechat_User.save()
    return message.content


def VoiceResponse(message):
    return 'VoiceMessage'


def ImageResponse(message):
    Image_Message = basic.PicMessage(to_user_name=message.target,
                                     from_user_name=message.source,
                                     create_time=message.time,
                                     message_type=message.type,
                                     message_id=message.id,
                                     media_id=message.media_id,
                                     pic_url=message.picurl)
    Image_Message.save()
    return 'get image %s' % message.picurl


def LinkResponse(message):
    Link_Message = basic.LinkMessage(to_user_name=message.target,
                                     from_user_name=message.source,
                                     create_time=message.time,
                                     message_type=message.type,
                                     message_id=message.id,
                                     title=message.title,
                                     description=message.description,
                                     url=message.url)
    Link_Message.save()
    return 'link:%s' % message.title


def LocationResponse(message):
    Iocation_Message = basic.LocationMessage(to_user_name=message.target,
                                             from_user_name=message.source,
                                             create_time=message.time,
                                             message_type=message.type,
                                             message_id=message.id,
                                             location_x=message.location[0],
                                             location_y=message.location[1],
                                             scale=message.scale,
                                             label=message.label)
    Iocation_Message.save()
    return 'location:x%s,y%s' % (message.location[0], message.location[1])


def VideoResponse(message):
    Video_Message = basic.VideoMessage(to_user_name=message.target,
                                       from_user_name=message.source,
                                       create_time=message.time,
                                       message_type=message.type,
                                       message_id=message.id,
                                       media_id=message.media_id,
                                       thumb_media_id=message.thumb_media_id)
    Video_Message.save()
    return 'VideoMessage:%s' % message.media_id


def ShortVideoResponse(message):
    ShortVideo_Message = basic.ShortVideoMessage(to_user_name=message.target,
                                                 from_user_name=message.source,
                                                 create_time=message.time,
                                                 message_type=message.type,
                                                 message_id=message.id,
                                                 media_id=message.media_id,
                                                 thumb_media_id=message.thumb_media_id)
    ShortVideo_Message.save()

    return 'ShortVideo_Message:%s' % message.media_id


def EventResponse(message,wechat_instance):
    if message.type == 'subscribe':  # 关注事件(包括普通关注事件和扫描二维码造成的关注事件)
        key = message.key  # 对应于 XML 中的 EventKey (普通关注事件时此值为 None)
        ticket = message.ticket  # 对应于 XML 中的 Ticket (普通关注事件时此值为 None)
        return 'key:%s-ticket:%s' % (key, ticket)

    elif message.type == 'unsubscribe':  # 取消关注事件（无可用私有信息）
        pass
    elif message.type == 'scan':  # 用户已关注时的二维码扫描事件
        key = message.key  # 对应于 XML 中的 EventKey
        ticket = message.ticket  # 对应于 XML 中的 Ticket

    elif message.type == 'location':  # 上报地理位置事件
        latitude = message.latitude  # 对应于 XML 中的 Latitude
        longitude = message.longitude  # 对应于 XML 中的 Longitude
        precision = message.precision  # 对应于 XML 中的 Precision
        location_Event = basic.LocationEvent(to_user_name=message.target,
                                             from_user_name=message.source,
                                             create_time=message.time,
                                             message_type=message.type,
                                             event=message.type,
                                             latitude=message.latitude,
                                             longitude=message.longitude,
                                             precision=message.precision)
        location_Event.save()
        reply_text='precision:%s-latitude:%s-longitude:%s' % (precision, latitude, longitude)
        return wechat_instance.response_text(content=reply_text)
    elif message.type == 'click':  # 自定义菜单点击事件
        try:
            print  message.source
            sendmessage = templatesend.SendMessage
            return_mes = sendmessage.objects.all().filter(author=message.source, status='0').order_by(
                'publish')[:5]
            articles = [{'title': i.title,
                         'picurl': 'http://pic10.huitu.com/res/20130531/169904_20130531201335309170_1.jpg',
                         'description': i.description, 'url': i.url} for i in return_mes]
            # articles = [{'title': 'this is test', 'description': 'its good',
            #              'url': 'http://widen-zhouzw.rhcloud.com'}]
            # response = wechat_instance.response_news(articles)

            for mes in return_mes:
                mes.status = '2'
                mes.save()
            # mmes=return_mes.values_list('pk')
            # sendmessage.objects.filter(pk__in=list(mmes)).update(status='2')
            return wechat_instance.response_news(articles)
        except Exception as e:
            print e
    elif message.type == 'view':  # 自定义菜单跳转链接事件
        key = message.key
        print message.key
        Menu_Event = basic.MenuEvent(to_user_name=message.target,
                                     from_user_name=message.source,
                                     create_time=message.time,
                                     message_type=message.type,
                                     event=message.type,
                                     event_key=message.key)
        Menu_Event.save()
        reply_text='view-key:%s' % key  # 对应于 XML 中的 EventKey
        return wechat_instance.response_text(content=reply_text)
    elif message.type == 'templatesendjobfinish':  # 模板消息事件
        status = message.status
        print message.MsgID
        Template_Event = basic.TemplateEvent(to_user_name=message.target,
                                             from_user_name=message.source,
                                             create_time=message.time,
                                             message_type=message.type,
                                             msgid=message.MsgID,
                                             event=message.type,
                                             status=message.status
                                             )
        Template_Event.save()
        reply_text=status  # 对应于 XML 中的 Status
        return wechat_instance.response_text(content=reply_text)

    elif message.type in ['scancode_push', 'scancode_waitmsg', 'pic_sysphoto',
                          'pic_photo_or_album', 'pic_weixin', 'location_select']:  # 其他事件
        reply_text = message.key
        return wechat_instance.response_text(content=reply_text)
    else:
        reply_text = 'other'
        return wechat_instance.response_text(content=reply_text)


ResponseFun = {
    'TextMessage': TextResponse,
    'VoiceMessage': VoiceResponse,
    'ImageMessage': ImageResponse,
    'VideoMessage': VideoResponse,
    'LinkMessage': LinkResponse,
    'LocationMessage': LocationResponse,
    'EventMessage': EventResponse,
    'ShortVideoMessage': ShortVideoResponse,
}
