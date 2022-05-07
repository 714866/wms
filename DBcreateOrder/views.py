from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
import os
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from  modular import mapper
from modular.PSR.CreateWspPSR import CreateWspPSR
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
    post_data['source_process_id']=post.get('source_process_id')
    post_data['targer_process_id']=post.get('targer_process_id')
    post_data['sku_code']=post.get('sku_code')
    post_data['oa_url']=post.get('url')
    post_data['cookie']=post.get('cookie')
    post_data['goods_type']=post.get('goods_type')
    find_goods_code = goodsSql()
    num=10   #执行次数
    # 处理产品
    if post.get('sku_code')[0:3].upper()=="SKU":
        post_data['sku_code'] = post.get('sku_code')
        post_data['sku_id'] = find_goods_code.findOaGoodsBySku(post.get('sku_code'))
        post_data['poa_code'] = ''
        post_data['poa_id'] = ''
    else:
        poa_code= post.get('sku_code')
        post_data['poa_code'] = poa_code
        try:
            goods_message=find_goods_code.findOaGoodsByPoa(poa_code)
        except TypeError:
            print('产品信息为空')
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
    try:
        api_action= createPSR(post_data['cookie'], post_data['oa_url'])
    except:
        return JsonResponse({'psr': '请求失败'})
    result = api_action.postPsr(post_data, num)
    print(result.text)
    psr_codes = sqlServerConnect(num)
    put_wsp_db = CreateWspPSR().psr_create_pck(psr_codes)
    return JsonResponse({'psr': psr_codes})



def page_not_found(request):
    return redirect('http://127.0.0.1:8000/DBcreateOrder/index/')


def sqlServerConnect(top_num):

    cursor = mapper.connect_sqlserve()
    select_psr = 'select top {} ShiftRequestID,ProductShiftRequestitem from ProductShiftRequest order by id desc'
    psrs = cursor.fetchall(select_psr.format(top_num))
    psr_ids = ''
    psr_codes = []
    count = 0
    for psr in psrs:
        psr_codes.append(psr['ProductShiftRequestitem'])
        psr_id = psr['ShiftRequestID']
        if count < top_num-1:
            psr_ids = psr_ids + psr_id+','
        else:
            psr_ids = psr_ids + psr_id
    # updateSql = 'update ProductShiftRequest set bStatus=1 , AuditState=2 where ShiftRequestID in (select top 10 ShiftRequestID from ProductShiftRequest order by ShiftRequestID desc ); '
    updateSql = 'update ProductShiftRequest set bStatus=1 , AuditState=2 where ShiftRequestID in ({0}); '.format(psr_ids)
    cursor.execute(updateSql)
    cursor.commitAndClose()
    return psr_codes

