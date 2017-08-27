# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
import wechat.models.wechat_menu


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AccessToken',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('corpid', models.CharField(default=b'wx1ac674deefe5da12', max_length=200)),
                ('corpsecret', models.CharField(default=b'5bc1c8a130cd1739bbae9e0234b98807', max_length=200)),
                ('token', models.CharField(default=b'python', max_length=1000)),
                ('aeskey', models.CharField(default=b'klsdjfkljlksdf', max_length=1000)),
                ('create_time', models.DateTimeField(default=datetime.datetime.now)),
                ('accesstoken', models.CharField(default=b'', max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='addinfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.CharField(max_length=500)),
                ('title', models.CharField(max_length=2000)),
                ('add_datetime', models.DateTimeField(auto_now=True)),
                ('user_id', models.CharField(max_length=200)),
                ('order_id', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='BasicEvent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('to_user_name', models.CharField(default=b'', max_length=500)),
                ('from_user_name', models.CharField(default=b'', max_length=500)),
                ('create_time', models.CharField(default=b'', max_length=500)),
                ('message_type', models.CharField(default=b'', max_length=500)),
                ('event', models.CharField(default=b'', max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='BasicMessage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('to_user_name', models.CharField(default=b'', max_length=500)),
                ('from_user_name', models.CharField(default=b'', max_length=500)),
                ('create_time', models.CharField(default=b'', max_length=500)),
                ('message_type', models.CharField(default=b'', max_length=500)),
                ('message_id', models.CharField(default=b'', max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='MessageAutoReplay',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content', models.CharField(default=b'', max_length=500)),
                ('rule', models.CharField(default=b'', max_length=500)),
                ('create_time', models.DateTimeField(default=datetime.datetime.now)),
            ],
        ),
        migrations.CreateModel(
            name='SendMessage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=250)),
                ('url', models.CharField(max_length=250)),
                ('description', models.TextField()),
                ('publish', models.DateField(default=b'')),
                ('template_id', models.CharField(max_length=250)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(default=b'wait', max_length=10, choices=[(b'0', b'Wait'), (b'1', b'Published'), (b'2', b'Success')])),
            ],
            options={
                'ordering': ('-publish',),
            },
        ),
        migrations.CreateModel(
            name='SendToUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('message_id', models.CharField(max_length=100)),
                ('openid', models.SlugField(max_length=250)),
                ('group_id', models.SlugField(max_length=250)),
                ('plan_date', models.DateTimeField(auto_now_add=True)),
                ('send_time', models.DateTimeField(auto_now_add=True)),
                ('mask', models.TextField()),
                ('status', models.CharField(default=b'0', max_length=10, choices=[(b'0', b'Ready'), (b'1', b'Send'), (b'3', b'Success'), (b'4', b'Fail')])),
            ],
        ),
        migrations.CreateModel(
            name='TemplateidInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('template_id', models.CharField(max_length=100)),
                ('template_desc', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='TopLevelMenu',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(default=b'click', max_length=10)),
                ('name', models.CharField(default=b'test', max_length=50)),
                ('key', models.CharField(default=wechat.models.wechat_menu.convert_uuid_to_string, max_length=100)),
                ('url', models.CharField(default=b'', max_length=1000)),
                ('sub_menu', models.CharField(max_length=1000, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='WechatOpenid',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('openid', models.CharField(default=b'', max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='WeChatServer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('server_ip_list', models.CharField(default=b'', max_length=1000, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='WechatUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('subscribe', models.CharField(default=b'', max_length=20)),
                ('openid', models.CharField(default=b'', unique=True, max_length=20)),
                ('nickname', models.CharField(default=b'', max_length=200)),
                ('sex', models.CharField(default=b'', max_length=20)),
                ('city', models.CharField(default=b'', max_length=40)),
                ('country', models.CharField(default=b'', max_length=40)),
                ('province', models.CharField(default=b'', max_length=40)),
                ('language', models.CharField(default=b'', max_length=20)),
                ('headimgurl', models.CharField(default=b'', max_length=100)),
                ('subscribe_time', models.CharField(default=b'', max_length=50)),
                ('unionid', models.CharField(default=b'', max_length=40)),
                ('remark', models.CharField(default=b'', max_length=100)),
                ('groupid', models.CharField(default=b'', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='KeFuMessage',
            fields=[
                ('basicmessage_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='wechat.BasicMessage')),
                ('message_content', models.TextField(default=b'')),
            ],
            bases=('wechat.basicmessage',),
        ),
        migrations.CreateModel(
            name='LinkMessage',
            fields=[
                ('basicmessage_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='wechat.BasicMessage')),
                ('title', models.CharField(default=b'', max_length=1000)),
                ('description', models.CharField(default=b'', max_length=1000)),
                ('url', models.CharField(default=b'', max_length=1000)),
            ],
            bases=('wechat.basicmessage',),
        ),
        migrations.CreateModel(
            name='LocationEvent',
            fields=[
                ('basicevent_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='wechat.BasicEvent')),
                ('latitude', models.CharField(default=b'', max_length=500)),
                ('longitude', models.CharField(default=b'', max_length=500)),
                ('precision', models.CharField(default=b'', max_length=500)),
            ],
            bases=('wechat.basicevent',),
        ),
        migrations.CreateModel(
            name='LocationMessage',
            fields=[
                ('basicmessage_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='wechat.BasicMessage')),
                ('location_x', models.CharField(default=b'', max_length=1000)),
                ('location_y', models.CharField(default=b'', max_length=1000)),
                ('scale', models.CharField(default=b'', max_length=500)),
                ('label', models.CharField(default=b'', max_length=1000)),
            ],
            bases=('wechat.basicmessage',),
        ),
        migrations.CreateModel(
            name='MenuEvent',
            fields=[
                ('basicevent_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='wechat.BasicEvent')),
                ('event_key', models.CharField(default=b'', max_length=500)),
            ],
            bases=('wechat.basicevent',),
        ),
        migrations.CreateModel(
            name='PicMessage',
            fields=[
                ('basicmessage_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='wechat.BasicMessage')),
                ('pic_url', models.CharField(default=b'', max_length=1000)),
                ('media_id', models.CharField(default=b'', max_length=1000)),
            ],
            bases=('wechat.basicmessage',),
        ),
        migrations.CreateModel(
            name='ScanQRcodeEvent',
            fields=[
                ('basicevent_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='wechat.BasicEvent')),
                ('event_key', models.CharField(default=b'', max_length=500)),
                ('ticket', models.CharField(default=b'', max_length=500)),
            ],
            bases=('wechat.basicevent',),
        ),
        migrations.CreateModel(
            name='SmallVideoMessage',
            fields=[
                ('basicmessage_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='wechat.BasicMessage')),
                ('media_id', models.CharField(default=b'', max_length=1000)),
                ('thumb_media_id', models.CharField(default=b'', max_length=1000)),
            ],
            bases=('wechat.basicmessage',),
        ),
        migrations.CreateModel(
            name='TemplateEvent',
            fields=[
                ('basicevent_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='wechat.BasicEvent')),
                ('msgid', models.CharField(default=b'', max_length=500)),
                ('status', models.CharField(default=b'', max_length=500)),
            ],
            bases=('wechat.basicevent',),
        ),
        migrations.CreateModel(
            name='TextMessage',
            fields=[
                ('basicmessage_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='wechat.BasicMessage')),
                ('message_content', models.TextField(default=b'')),
            ],
            bases=('wechat.basicmessage',),
        ),
        migrations.CreateModel(
            name='VideoMessage',
            fields=[
                ('basicmessage_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='wechat.BasicMessage')),
                ('media_id', models.CharField(default=b'', max_length=1000)),
                ('thumb_media_id', models.CharField(default=b'', max_length=1000)),
            ],
            bases=('wechat.basicmessage',),
        ),
        migrations.CreateModel(
            name='VoiceMessage',
            fields=[
                ('basicmessage_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='wechat.BasicMessage')),
                ('media_id', models.CharField(default=b'', max_length=1000)),
                ('format', models.CharField(default=b'', max_length=20)),
            ],
            bases=('wechat.basicmessage',),
        ),
        migrations.AddField(
            model_name='sendmessage',
            name='author',
            field=models.ForeignKey(to='wechat.WechatUser', to_field=b'openid'),
        ),
    ]
