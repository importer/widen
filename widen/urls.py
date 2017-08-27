from django.conf.urls import include, url
from django.contrib import admin

from welcome.views import index, health
from index import views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^wechat/', include('wechat.urls',namespace='wechat')),
    url(r'^index/', include('index.urls',namespace='index')),
    url(r'^accounts/', include('accounts.urls',namespace='accounts')),
    url(r'^$', views.index,name='index'),
    url(r'^health$', health),
    url(r'^admin/', include(admin.site.urls)),
]