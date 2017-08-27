# coding=utf8
import datetime
import MySQLdb

conn=MySQLdb.connect(
        host='127.5.110.130',
        port=3306,
        user='adminidCfHvr',
        passwd='AzM3ldIVFxY2',
        db='widen',
        charset='utf8',
    )


def insertinto_message(messages):
    '''插入消息到数据库'''
    start_time = datetime.datetime.now()
    # + datetime.timedelta(days=1)
    # .strftime("%Y-%m-%d")
    # listss=[(duo[0],duo[1],(start_time + datetime.timedelta(days=i+1)).strftime("%Y-%m-%d")) for i,duo in enumerate(get_message1())]
    # messages = get_message()
    listss = [(duo[0], duo[1],duo[2],duo[3], (start_time + datetime.timedelta(days=i)).strftime("%Y-%m-%d")) for i, duo in
              enumerate(messages)]
    # listss = [(duo[0], duo[1],duo[2],duo[3], (start_time + datetime.timedelta(days=i - 30)).strftime("%Y-%m-%d"),'NhAjvkKejw9ZFACNCjQCFNhsrsui0tKA5HGl7HetWZQ',start_time,start_time,1) for i, duo in
    #           enumerate(messages)]
    # print listss
    cur = conn.cursor()
    cur.executemany('''INSERT INTO index_post (title,author,url,description,publish)VALUES (?,?,?,?,?)''', listss)
    # cur.executemany('''INSERT INTO wechat_sendmessage (title,author,url,description,publish,template_id,created,updated,status)VALUES (?,?,?,?,?,?,?,?,?)''', listss)
    conn.commit()
    cur.close()

def get_send():
    '''title,author,url,description,publish,model_id'''
    now = datetime.datetime.now().strftime("%Y-%m-%d")
    sql = 'select title,author,url,description,publish from wechat_sendmessage where publish=\'{date_now}\''.format(
        date_now=now)
    cur = conn.cursor()
    cur.execute(sql)
    send_message = cur.fetchall()
    cur.close()
    return send_message


def update_log(url):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sql = 'update wechat_sendmessage set updated=\'{now}\',status=\'success\' where  url=\'{url}\''.format(
        url=url, now=now)
    # print sql
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    cur.close()


if __name__ == '__main__':
    print get_send()
