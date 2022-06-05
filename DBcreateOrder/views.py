import json

from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
import os
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from  modular import mapper
from modular.PSR.CreateWspPSR import CreateWspPSR
from  modular.PSR.createPSR import createPSR
from modular.SFT.createSftInstorageRequest import CreateSfiInstorageRequest
from modular.goods.OAGoods import goodsSql
from modular.oaDB.getPsr import PsrMessage

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
    if post.__len__()==0 :
        post=json.loads(request.body)
    post_data={}
    post_data['source_process_id']=post.get('source_process_id')
    if post_data['source_process_id'] is None or post_data['source_process_id']=='':
        post_data['source_process_id'] = 1040
    post_data['targer_process_id']=post.get('targer_process_id')
    if post_data['targer_process_id'] is None or post_data['targer_process_id']=='':
        post_data['targer_process_id'] = 1111
    sku_code = post.get('sku_code')
    if sku_code is None or sku_code=='':
        sku_code ='POA4235465'
    post_data['sku_code']=sku_code
    post_data['oa_url']=post.get('url')
    if post_data['oa_url'] is None or  post_data['oa_url']=='':
        post_data['oa_url']='http://172.16.6.203:8092'
    post_data['storage']=post.get('storage')
    goods_type = post.get('goods_type')
    if goods_type is None or goods_type=='':
        goods_type=0
    post_data['goods_type'] = goods_type
    num=post.get('count_num')
    if num is None or num=='':
        num =10
    #执行次数
    post_data['count_num']=num
    product_num = post.get('product_num')
    if product_num is None or product_num=='':
        product_num=1
    post_data['product_num']=product_num
    # 处理产品
    find_goods_code = goodsSql()
    if sku_code[0:3].upper()=="SKU":
        post_data['sku_code'] = sku_code
        post_data['sku_id'] = find_goods_code.findOaGoodsBySku(sku_code)
        post_data['poa_code'] = ''
        post_data['poa_id'] = ''
    else:
        poa_code= sku_code
        post_data['poa_code'] = poa_code
        try:
            goods_message=find_goods_code.findOaGoodsByPoa(poa_code)
        except TypeError:
            print('产品信息为空')
        post_data['poa_id'] = goods_message['poa_id']
        post_data['sku_code'] = goods_message['sku_code']
        post_data['sku_id'] = goods_message['sku_id']
    #调用oa接口创建调拨请求
    try:
        api_action= createPSR( post_data['oa_url'])
        result = api_action.postPsr(post_data)
    except BaseException as  err:
        return JsonResponse({'psr': '请求失败{0}'.format(err)})
    print(result.text)
    # try:
    #更改生成的调拨单状态
    psr_codes = PsrMessage().updatePsrBstatus(num)
    print('oa创建成功，且修改调拨请求的bstatus状态')
    #wsp创建调拨请求与包裹单
    put_wsp_db = CreateWspPSR().psr_create_pck(psr_codes)
    # except BaseException as  err:
    #     return JsonResponse({'psr': '在wsp创建数据失败,请求失败{0}'.format(err)})

    return JsonResponse({'psr': put_wsp_db})



def InStorageRequest(request):
    """
    生成入库申请
    :param request:
    :return:
    """
    post = request.POST
    post_data = {}
    post_data['sft_code'] = post.get('sft_code')
    isr = CreateSfiInstorageRequest()
    wms_code = isr.createIsrRequestToWms(post.get('sft_code'))
    print('创建入库单成功的单据{0}'.format(wms_code))
    return wms_code

def page_not_found(request):
    return redirect('http://127.0.0.1:8000/DBcreateOrder/index/')


# def sqlServerConnect(top_num):
#
#     cursor = mapper.connect_sqlserve()
#     select_psr = 'select top {0} ShiftRequestID,ProductShiftRequestitem from ProductShiftRequest where bStatus=0 order by id desc'
#     psrs = cursor.fetchall(select_psr.format(top_num))
#     psr_ids = ''
#     psr_codes = []
#     count = 0
#     for psr in psrs:
#         psr_codes.append(psr['ProductShiftRequestitem'])
#         psr_id = psr['ShiftRequestID']
#         if count < top_num-1:
#             psr_ids = psr_ids + psr_id+','
#         else:
#             psr_ids = psr_ids + psr_id
#     # updateSql = 'update ProductShiftRequest set bStatus=1 , AuditState=2 where ShiftRequestID in (select top 10 ShiftRequestID from ProductShiftRequest order by ShiftRequestID desc ); '
#     updateSql = 'update ProductShiftRequest set bStatus=1 , AuditState=2 where ShiftRequestID in ({0}); '.format(psr_ids)
#     cursor.execute(updateSql)
#     cursor.commitAndClose()
#
#     return psr_codes



