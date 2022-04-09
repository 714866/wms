from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
import os
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from  modular import mapper
from  modular.PSR.createPSR import createPSR


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
    """
    PSR创建
    :param request:
    :return:
    """
    post=request.POST
    source_process=post.get('source_process')
    targer_process=post.get('targer_process')
    sku_code=post.get('sku_code')
    oa_url=post.get('url')
    cookie=post.get('cookie')
    goods_type=post.get('goods_type')

    list=[]
    list.append(source_process)
    list.append(targer_process)
    list.append(sku_code)
    list.append(oa_url)
    list.append(cookie)
    list.append(goods_type)
    api_action=createPSR(oa_url,cookie)
    result=api_action.postPsr()
    print(result.text)
    sqlServerConnect(10)
    return JsonResponse({'psr':list})



def page_not_found(request):
    return redirect('http://127.0.0.1:8000/DBcreateOrder/index/')


def sqlServerConnect(top_num):

    cursor = mapper.connect_sqlserve()
    updateSql = 'update ProductShiftRequest set bStatus=1 , AuditState=2 where ShiftRequestID in (select top 10 ShiftRequestID from ProductShiftRequest order by ShiftRequestID desc ); '
    newId = cursor.execute(updateSql)

    cursor.commitAndClose()

