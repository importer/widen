from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from wechat.models import templatesend
from django.shortcuts import render
import json

@login_required
def checkbox(request):
    if request.method=='POST':
        # request.encoding = 'gb2312'
        post_data = request.POST.get('data')
        checkbox_list=json.loads(post_data)
        user_id=request.user
        # print 'the user id:%s'%user_id.id
        querysetlist = []
        addinfo = templatesend.addinfo
        for k, v in checkbox_list.items():
            querysetlist.append(addinfo(url=v[1], title=v[0],user_id=user_id.id,order_id=k))
        addinfo.objects.bulk_create(querysetlist)
        return HttpResponse('data submit success!')
    else:
        addinfos=[]
        request.encoding = 'gb2312'
        checkbox_list = request.GET
        user_id=request.user
        for k,v in checkbox_list.items():
            addinfos.append((k,v))
        return render(request,'addedit.html',{'addinfos':addinfos})

