#!/usr/bin/env python
# -*- coding:utf-8 -*-
import urllib2, json
import datetime, time
from config import *
import sys
from insert_message import *

reload(sys)
sys.setdefaultencoding("utf-8")


class WechatPush():
    def __init__(self, appid, secrect, file_name):
        # 传入appid
        self.appid = appid
        # 传入密码
        self.secrect = secrect
        # 传入记录token和过期时间的文件名
        self.file_name = file_name

    def build_timestamp(self, interval):
        # 传入时间间隔,得到指定interval后的时间 格式为"2015-07-01 14:41:40"
        now = datetime.datetime.now()
        delta = datetime.timedelta(seconds=interval)
        now_interval = now + delta
        return now_interval.strftime('%Y-%m-%d %H:%M:%S')

    def check_token_expires(self):
        # 判断token是否过期
        with open(self.file_name, 'r') as f:
            line = f.read()
            if len(line) > 0:
                expires_time = line.split(",")[1]
                token = line.split(",")[0]
            else:
                return "", "false"
        curr_time = time.strftime('%Y-%m-%d %H:%M:%S')
        # 如果过期返回false
        if curr_time > expires_time:
            return token, "false"
        # 没过期返回true
        else:
            return token, "true"

    def getToken(self):
        # 获取accessToken
        url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=' + self.appid + "&secret=" + self.secrect
        try:
            f = urllib2.urlopen(url)
            s = f.read()
            # 读取json数据
            j = json.loads(s)
            j.keys()
            # 从json中获取token
            token = j['access_token']
            print 'this is {0}'.format(token)
            # 从json中获取过期时长
            expires_in = j['expires_in']
            # 将得到的过期时长减去300秒然后与当前时间做相加计算然后写入到过期文件
            write_expires = self.build_timestamp(int(expires_in - 300))
            content = "%s,%s" % (token, write_expires)
            with open(self.file_name, 'w') as f:
                f.write(content)
        except Exception, e:
            print e
        return token

    def post_data(self, url, para_dct):
        """触发post请求微信发送最终的模板消息"""
        para_data = para_dct
        f = urllib2.urlopen(url, para_data)
        content = f.read()
        return content

    def do_push(self, touser, template_id, url, topcolor, data):
        '''推送消息 '''
        # 获取存入到过期文件中的token,同时判断是否过期
        token, if_token_expires = self.check_token_expires()
        # 如果过期了就重新获取token
        if if_token_expires == "false":
            token = self.getToken()
        # 背景色设置,貌似不生效
        if topcolor.strip() == '':
            topcolor = "#7B68EE"
        # 最红post的求情数据
        dict_arr = {'touser': touser, 'template_id': template_id, 'url': url, 'topcolor': topcolor, 'data': data}
        json_template = json.dumps(dict_arr)
        requst_url = "https://api.weixin.qq.com/cgi-bin/message/template/send?access_token=" + token
        content = self.post_data(requst_url, json_template)
        # 读取json数据
        j = json.loads(content)
        j.keys()
        errcode = j['errcode']
        errmsg = j['errmsg']
        print errcode, errmsg


def send_message(title, author, url, content, publish):
    '''发送信息：title,url,content,author,publish'''
    timestap = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    data = {"first": {"value": title},
            "keyword1": {"value": author, "color": color},
            "keyword2": {"value": content,
                         "color": color},
            "keyword3": {"value": publish.strftime("%Y-%m-%d"), "color": color},
            "remark": {"value": '期待下一个'}}
    # 实例化类
    webchart = WechatPush(appid, secrect, file_name)
    # 发送消息
    webchart.do_push(touser, template_id, url, "", data)


def main():
    for title, author, url, description, publish in get_send():
        # print title, author, url, description, publish, model_id
        send_message(title, author, url, description, publish)
        # 更新日志
        update_log(url)

if __name__ == "__main__":
    print u'开始'
    main()
    # pro_cons()
