__author__ = 'zhouzw'
from django.conf.urls import url
from index import views

urlpatterns = [
    url(r'^weui/', views.weui, name='weui'),
    url(r'^register/', views.register, name='register'),
    url(r'^userinfo/', views.userinfo, name='userinfo'),
    url(r'^base/', views.base, name='base'),
    url(r'^datail/', views.get_detail, name='datail'),
    url(r'^uploader/', views.uploader, name='uploader'),
    url(r'^test/', views.test, name='test'),
    url(r'^add$', views.addUserSubmit, name='addUserSubmit'),
    url(r'^infolist/', views.InfoListView.as_view(), name='InfoListView'),
    url(r'^infodetail/(?P<pk>[0-9]+)/$', views.InfoDetail.as_view(), name='detail'),
]
