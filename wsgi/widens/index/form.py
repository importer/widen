#coding=utf-8
__author__ = 'zhouzw'
from django  import forms
from index.models import UserSubmit
from django.forms import Textarea,DateInput,TextInput,Select

class Usersubmit(forms.ModelForm):
    class Meta:
        model=UserSubmit
        # fields=('title','url','plandate','rule','description','select_user')
        fields='__all__'
        widgets = {
            'title': TextInput(attrs={'class': 'weui_input','placeholder':'请输入标题'}),
            'url': TextInput(attrs={'class': 'weui_input','type':'url','placeholder':'请输入URL'}),
            'plandate': DateInput(attrs={'class': 'weui_input','type':'date'}),
            'rule': TextInput(attrs={'class': 'weui_input','placeholder':'请输入标题'}),
            'description': Textarea(attrs={'class': 'weui_textarea','placeholder':'描述','rows':'3'}),
            'select_user': Select(attrs={'class': 'weui_select','placeholder':'选择用户'}),
                   }