import json
import time

from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
import os
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from  modular import mapper
from modular.PSR.CreateWspPSR import CreateWspPSR
from  modular.PSR.createPSR import createPSR
from modular.SFT.createSftInstorageRequest import CreateSfiInstorageRequest
from modular.SFT.enums.shiptype import ShipType
from modular.common.craetecode import GetCode
from modular.goods.OAGoods import goodsSql
from modular.oaDB.getPsr import PsrMessage

# Create your views here.


# 测试验证用  暂时无用
from modular.wspDB.instoragerequest import InstorageMessage


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
    print('请求开始，验证是否重复请求的')
    post=request.POST
    if post.__len__()==0 :
        post=json.loads(request.body)
    post_data={}
    post_data['ship_type']=post.get('ship_type')
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
        num =5
    #执行次数
    post_data['count_num']=num
    product_num = post.get('product_num')
    if product_num is None or product_num=='':
        product_num=1
    post_data['product_num']=product_num
    # 处理产品
    find_goods_code = goodsSql()
    if sku_code[0:3].upper()=="POA":
        poa_code = sku_code
        post_data['poa_code'] = poa_code
        try:
            goods_message = find_goods_code.findOaGoodsByPoa(poa_code)
        except TypeError:
            print('产品信息为空')
        post_data['poa_id'] = goods_message['poa_id']
        post_data['sku_code'] = goods_message['sku_code']
        post_data['sku_id'] = goods_message['sku_id']
    else:
        post_data['sku_code'] = sku_code
        post_data['sku_id'] = find_goods_code.findOaGoodsBySku(sku_code)
        post_data['poa_code'] = ''
        post_data['poa_id'] = ''
    #调用oa接口创建调拨请求
    try:
        api_action= createPSR( post_data['oa_url'])
        result = api_action.postPsr(post_data)
    except AssertionError as  err:
        return JsonResponse({'psr': '请求失败{0}'.format(err)})
    print(result.text)
    try:
    #更改生成的调拨单状态
        psr_codes = PsrMessage().updatePsrBstatus(num)
        print('oa创建成功，且修改调拨请求的bstatus状态')
        #wsp创建调拨请求与包裹单
        put_wsp_db = CreateWspPSR().psr_create_pck(psr_codes)
    except AssertionError as  err:
        return JsonResponse({'psr': '{0}'.format(err)})

    return JsonResponse({'psr': put_wsp_db})


@csrf_exempt
def InStorageRequest(request):
    """
    生成入库申请
    :param request:
    :return:
    """
    post = request.POST
    if post.__len__() == 0:
        post = json.loads(request.body)
    post_data = {}
    post_data['sft_code'] = post.get('sft_code')
    isr = CreateSfiInstorageRequest()
    wms_code = isr.createIsrRequestToWms(post.get('sft_code'))
    print('创建入库单成功的单据{0}'.format(wms_code))
    return JsonResponse({'wms_code': list(wms_code)})

@csrf_exempt
def virtualInStorageRequest(request):
    """
{
	"goods_code":"PBUC01BBCAD",
	"quantity":3,
	"processcenter_id":1138,
	"shipType":3,   -- 传入

    :param request:
    :return:
    """
    post = request.POST
    if post.__len__() == 0:
        post = json.loads(request.body)
    post_datas = []
    post_data = {}
    post_data['quantity'] = post.get('quantity')
    post_data['originProcessCenterId'] = post.get('processcenter_id')
    post_data['targetProcessCenterId'] = post.get('processcenter_id')
    find_goods_code = goodsSql()
    wsp_db =InstorageMessage()
    post_data['baseProductCode'] = post.get('goods_code')
    start_code = post_data['baseProductCode'][0:3].upper()
    if start_code=="PBU":
        # 未完成，后续补逻辑
        goods_message = wsp_db.findGoodsInfo( post_data['baseProductCode'])
        post_data['propertyId'] = goods_message['property_id']
        post_data['productId'] = goods_message['product_id']
        if goods_message['property_id']=='0':
            post_data['baseProductCode'] = goods_message['product_code']
        else:
            post_data['baseProductCode'] = goods_message['property_code']
        pass
    elif  start_code == "POA":
        try:
            goods_message = find_goods_code.findOaGoodsByPoa(post_data['goods_code'])
        except TypeError:
            print('产品信息为空')
        post_data['propertyId'] = goods_message['poa_id']
        post_data['productId'] = goods_message['sku_id']
    else:
        post_data['sku_id'] = find_goods_code.findOaGoodsBySku(post_data['goods_code'])
        post_data['PropertyCode'] = ''
        post_data['poa_id'] = ''
    nowDate = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    post_data['modifyTimeStamp'] = nowDate

    # 自建单号SFT-T1-日期 ,暂时只做单条的逻辑
    get_code = GetCode()
    sft_codes = get_code.getSftCode(1)
    post_data['originCode']=sft_codes[0]
    #自建分箱单号
    box_codes = get_code.getboxCode(1)
    post_data['productShiftBoxCode']=box_codes[0]
    # 调拨单的来源单号，后面再看看是否可以传空
    post_data['productShitItemOriginCode']=''
    #运输方式
    post_data['shipType'] = ShipType(post.get('shipType')).name
    #货位类型
    post_data['goodsType'] = post.get('goodsType')
    post_data['length']='120'
    post_data['width']='120'
    post_data['height']='120'
    post_data['weight']='120'
    #可为空的 暂时就直接赋值空
    post_data['storageCode']=''
    post_data['deliveryProductCode']=''
    post_data['amazonShop']=''
    post_data['detailLabel']=''
    post_data['relativeCode']=''
    post_data['traceCode']=''
    post_data['logId']=''
    post_data['goodsSize']=''
    post_data['fboxItemOriginCode']=''
    post_data['type']=''
    post_data['ful']=False
    post_datas.append(post_data)
    isr = CreateSfiInstorageRequest()
    # 组装参数
    create_info = isr.wspApiMessages(post_datas)
    wms_codes = isr.syncFromProductShiftInfo(create_info)
    return JsonResponse({'wms_code': wms_codes})



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



