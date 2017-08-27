#!/usr/bin/python
#-*-coding:UTF-8-*-
import smtplib
from email.mime.text import MIMEText

def send_mail(to_list,user,sub,content):
    
    mail_host="smtp.163.com"            #使用的邮箱的smtp服务器地址，这里是163的smtp地址
    mail_user="bigbigsman"                           #用户名
    mail_postfix="163.com"                     #邮箱的后缀，网易就是163.com

    me=user+"<"+mail_user+"@"+mail_postfix+">"
    msg = MIMEText(content,_subtype='plain',_charset='utf-8')
    msg['Subject'] = sub
    msg['From'] = me
    msg['To'] = ";".join(to_list)                #将收件人列表以‘；’分隔
    try:
        server = smtplib.SMTP()
        server.connect(mail_host)                            #连接服务器
        server.login("bigbigsman@163.com","sun25879")    #登录操作,密码是授权码，而不是邮箱登录密码
        server.sendmail(me, to_list, msg.as_string())
        server.close()
        return True
    except Exception, e:
        print str(e)
        return False
def send_qq(to_list,sub,content):
    _user = "2250093397@qq.com"
    _pwd  = "rkjddwaeieyfdhic"
    msg = MIMEText(content,_subtype='plain',_charset='utf-8')
    msg['Subject'] = sub
    msg['From'] = _user
    msg['To'] = ";".join(to_list)                #将收件人列表以‘；’分隔
    # msg['To'] =   '18314558441@139.com'              #将收件人列表以‘；’分隔
    try:
        s = smtplib.SMTP_SSL("smtp.qq.com", 465)
        s.login(_user, _pwd)
        s.sendmail(_user, to_list, msg.as_string())
        s.quit()
        print "Success!"
    except smtplib.SMTPException,e:
        print "Falied,%s"%e 
def mail_to(sub,content):
    '''    
    #16    part1 = ''
    #60    part2 = ''
    #37    part3 = ''
    '''
    mailto_list=['18314558441@139.com']           #收件人(列表)
    # if send_mail(mailto_list,part1,part2,part3):  #邮件主题和邮件内容
    #     return "done!"
    send_qq(mailto_list,sub,content)  #邮件主题和邮件内容

if __name__ == '__main__':
    mail_to('快乐的小小鸟','20170119成功插入：31条,机会总是留给有准备的人！')    