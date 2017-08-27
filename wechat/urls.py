__author__ = 'zhouzw'
from django.conf.urls import url
from wechat.views import basic,menu,index

urlpatterns = [
    url(r'^menu/$', menu.create_menu_admin,name='create_menu'),
    url(r'^weixin_web/$', basic.weixin_web,name='weixin_web'),
    url(r'^admin_dashboard/$', basic.admin_dashboard,name='admin_dashboard'),
    url(r'^send_template/$', basic.send_template,name='send_template'),
    url(r'^checkbox/$', index.checkbox,name='checkbox'),
    url(r'^$', basic.index,name='index'),
]