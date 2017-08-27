# coding=utf-8
import logging
from widens import settings
import requests
from index.models import *


class WeiXinLogin():
    def __init__(self, code, state):
        self.code = code
        self.state = state
        self.appid = settings.APP_ID
        self.appsecret = settings.APP_SECRET
        self.access_token = ''
        self.refresh_token = ''
        self.openid = ''
        self.is_expires = 1
        self.detail = {}

    # 为了方便大家看,我都写在一个函数里
    def get_access_token(self):
        # 2.通过code换取网页授权access_token
        if self.refresh_token:
            url = u'https://api.weixin.qq.com/sns/oauth2/refresh_token'
            params = {
                'appid': self.appid,
                'grant_type': self.refresh_token,
                'refresh_token': self.refresh_token
            }
            res = requests.get(url, params=params).json()
            if res.get('errcode', None):
                logging.info(res.get('errmsg'))
                return res.get('errmsg')
            self.access_token = res.get("access_token")
            self.openid = res.get("openid")
            self.refresh_token = res.get('refresh_token')
            logging.info(
                'access_token:%s ;openid:%s ;refresh_token:%s' % (
                    self.access_token, self.openid, self.refresh_token))
            return True
        url = u'https://api.weixin.qq.com/sns/oauth2/access_token'
        params = {
            'appid': self.appid,
            'secret': self.appsecret,
            'code': self.code,
            'grant_type': 'authorization_code'
        }
        res = requests.get(url, params=params).json()
        if res.get('errcode', None):
            logging.info(res.get('errmsg'))
            return res.get('errmsg')
        self.access_token = res.get("access_token")
        self.openid = res.get("openid")
        self.refresh_token = res.get('refresh_token')
        Token_get = Token(**res)
        Token_get.save()
        logging.info(
            'access_token:%s ;openid:%s ;refresh_token:%s' % (
                self.access_token, self.openid, self.refresh_token))
        return True

    def token_expires(self):
        # 监测当前access_token是否超时？
        url = u'https://api.weixin.qq.com/sns/auth'
        params = {
            'appid': self.appid,
            'access_token': self.access_token,
        }
        res = requests.get(url, params=params).json()
        if res.get('errcode'):
            self.is_expires = 1
            logging.info('is_expires:%s' % self.is_expires)
        else:
            self.is_expires = 0
        return True

    def get_info(self):
        # 4.拉取用户信息
        user_info_url = u'https://api.weixin.qq.com/sns/userinfo'
        params = {
            'access_token': self.access_token,
            'openid': self.openid,
            'lang': 'zh_CN',
        }
        res = requests.get(user_info_url, params=params).json()
        if res.get('errcode'):
            return res.get('errmsg')
        # decode response content
        logging.info('Get user detail openid:' + res.get('openid'))
        for key, value in res.items():
            self.detail[key] = value.encode('iso8859-1').decode('utf-8') if isinstance(value, str)  else  value
        WxUser = Wxuser(**self.detail)
        WxUser.save()
        logging.info('Save%s to db' % self.detail.get('openid'))
        return True

    def get_detail(self):
        self.token_expires()
        if self.is_expires == 1:
            self.get_access_token()
        self.get_info()
        return self.detail
