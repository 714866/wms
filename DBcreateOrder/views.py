from django.shortcuts import render
from django.http import HttpResponse
import os
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect

# Create your views here.


# 测试验证用  暂时无用
def create_order(request):
    return HttpResponse('create_order')


def index(request):
    # post=request.POST
    # uname=post.get('username')
    # upwd=post.get('pwd')
    # return render(request, 'df_user/login.html')
    #自己写的
    a=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    uname=request.COOKIES.get('uname','')
    error_name=request.COOKIES.get('error_name',0)
    error_pwd=request.COOKIES.get('error_pwd',0)
    context={
        'title':'test模块','error_name':error_name,'error_pwd':error_pwd,'uname':uname
    }
    return render(request,'DBcreateOrder/index.html',context)

@csrf_exempt
def returnResult(request):
    post=request.POST
    process=post.get('process')
    return_list=[]
    return_list.append('a')
    return_list.append('b')

    list=[]
    list.append('a')
    list.append('b')
    return JsonResponse({'psr':list})

import pymssql
def sqlServerConnect():
    conn = pymssql.connect(server, user, password, database)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM persons WHERE salesrep=%s', 'John Doe')
    row = cursor.fetchone()
    while row:
        print("ID=%d, Name=%s" % (row[0], row[1]))
        row = cursor.fetchone()