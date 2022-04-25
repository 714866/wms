from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
import os
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from  modular import mapper
from  modular.PSR.createPSR import createPSR
from modular.goods.OAGoods import goodsSql


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
    post_data={}
    post_data['source_process']=post.get('source_process')
    post_data['targer_process']=post.get('targer_process')
    post_data['sku_code']=post.get('sku_code')
    post_data['oa_url']=post.get('url')
    post_data['cookie']=post.get('cookie')
    post_data['goods_type']=post.get('goods_type')
    find_goods_code = goodsSql()
    # 处理产品
    if post.get('sku_code')[0:3].upper()=="SKU":
        post_data['sku_code'] = post.get('sku_code')
        post_data['sku_id'] = find_goods_code.findOaGoodsBySku(post.get('sku_code'))
        post_data['poa_code'] = ''
        post_data['poa_id'] = ''
    else:
        poa_code=find_goods_code.findOaGoodsByPoa()
        post_data['poa_code'] = poa_code
        goods_message=find_goods_code.findOaGoodsByPoa(poa_code)
        post_data['poa_id'] = goods_message['poa_id']
        post_data['sku_code'] = goods_message['sku_code']
        post_data['sku_id'] = goods_message['sku_id']
    # list=[]
    # list.append(source_process)
    # list.append(targer_process)
    # list.append(sku_code)
    # list.append(oa_url)
    # list.append(cookie)
    # list.append(goods_type)
    api_action= createPSR(post_data['cookie'], post_data['oa_url'])
    result=api_action.postPsr(post_data)
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

