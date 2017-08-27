# coding=utf-8
import requests
import re
import time
import MySQLdb


link_list = set()
# 链接数据库


def connect_db():
    # return sqlite3.connect(app.config['DATABASE'])
    return MySQLdb.connect(
        host='575babcb7628e149b6000202-zhouzw.rhcloud.com',
        port=39671,
        user='adminSMzRDu3',
        passwd='Ci-CBgFGBzx7',
        db='import',
        charset='utf8',
    )
    # return MySQLdb.connect(
    #     host='127.0.0.1',
    #     port = 3306,
    #     user='root',
    #     passwd='root',
    #     db ='zhouzw',
    #     charset='utf8',
    #     )

# 初始化数据库（建立基本表）


def init_db():
    with closing(connect_db()) as db:
        with open('../schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

g_cursor = connect_db().cursor()
conn = connect_db()


def getdata(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.87 Safari/537.36'}
    res = requests.get(url, headers=headers)
    return res.text


def spider_jpg(res_url):
    # 获取网页内容
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.87 Safari/537.36'}
    content = requests.get(res_url, headers=headers).text
    # 获取图片链接
    pattern = '<img src="(.*?)"'
    # 获取下一页链接
    pattern_page = '<a title="Older Comments" href="(.*?)" class="previous-comment-page"'
    pattern = re.compile(pattern, re.S)
    pattern_page = re.compile(pattern_page, re.S)
    next_page = re.findall(pattern_page, content)
    src_list = re.findall(pattern, content)
    if len(src_list) < 2:
        return None
    for link in src_list:
        link_list.add(link)
    return next_page[0]


def spider_start():
    url = 'http://jandan.net/ooxx'
    now_date = time.strftime('%Y%m%d', time.localtime(time.time()))
    for i in range(10):
        url = spider_jpg(url)
        if url is None:
            return '内容为空！'
        lens = len(link_list)
        for i in range(lens):
            g_cursor.execute(
                'insert into jiandan_src(adddate,pic_url) values(%s,%s)', (now_date, link_list.pop()))
    connect_db().commit()
    return '{a}成功插入：{b}条'.format(a=now_date, b=lens)
# def i_have_a_dream(func, *args, **kwargs):
#     """
#     异步任务处理。本函数会立即返回，并使用 gevent 的新线程执行 func 函数（带 request 上下文）。
#     """
#     return gevent.spawn(copy_current_request_context(func), *args, **kwargs)
# def spider_start():
#     gevent.joinall([gevent.spawn(copy_current_request_context(jiandanspider))])
#     return 'The spider is start!!!'

