#coding=utf-8
from django.http import HttpResponseRedirect
#装饰，给未登录用户的在特点页面跳转到登陆界面
def login(func):
    def login_fun(request,*args,**kwargs):
        if request.session.get('user_id'):
            return func(request,*args,**kwargs)
        else:
            red=HttpResponseRedirect('/user/login/')
            print('sdfsdlkj')
            red.set_cookie('url',request.get_full_path())
            return red
    return login_fun