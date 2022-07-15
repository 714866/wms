import copy
import json
import time

from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
import os
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from  modular import mapper
from modular.PPL.createPPLInstorageRequest import CreatePPLInstorageRequest
from modular.PSR.CreateWspPSR import CreateWspPSR
from modular.PSR.createPSR import createPSR, CreateThirdPsr
from modular.SFT.createSftInstorageRequest import CreateSfiInstorageRequest
from modular.SFT.enums.shiptype import ShipType
from modular.SFT.sftflow import SftFlow
from modular.common.SqlChangeFormat import DateEncoder
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
def getPsr(request):
    post = request.POST
    if post.__len__() == 0:
        post = json.loads(request.body)
    try:
        psr_code = post.get('psr_codes')
        test_psr = CreateWspPSR()
        data = test_psr.get_oa_psr(psr_code)
        source_psr_codes = test_psr.put_wsp(data)
        operation_psr_codes = test_psr.source_to_operation(source_psr_codes)
        return JsonResponse({'psr': operation_psr_codes})
    except AssertionError as  err:
        return JsonResponse({'报错提示': '{0}'.format(err).replace('\n', '')})


@csrf_exempt
def thirdPsr(request):
    third_psr = CreateThirdPsr()
    post = request.POST
    if post.__len__() == 0:
        post = json.loads(request.body)
    post_data = {}
    post_data['customerLabel'] =post.get('goods_code')
    goods_code = post_data['customerLabel']
    find_goods_code = goodsSql()
    try:
        if goods_code[0:3].upper() == "POA":
            goods_message = find_goods_code.findOaGoodsByPoa(goods_code)
            post_data['propertyId'] = goods_message['poa_id']
            post_data['productId'] = goods_message['sku_id']
        else:
            post_data['productId'] = find_goods_code.findOaGoodsBySku(goods_code)
            post_data['propertyId'] = '0'
    except TypeError:
        print('产品信息为空')
        return JsonResponse({'error':'查询OA数据库，产品{0}信息为空'.format(goods_code)})
    post_data['goodsType'] =post.get('goodsType')
    post_data['shipType'] =post.get('shipType')
    post_data['deliveryProductCode'] =post.get('deliveryProductCode')
    post_data['shopName'] =post.get('shopName')
    post_data['quantity'] =post.get('quantity')
    post_data['processCenterId'] =post.get('TargetProcessCenterId')
    post_data['sourceProcessCenterId'] =post.get('OriginProcessCenterId')

    request_data = third_psr.thirdPsrApiMessages(post_data)
    try:
        result_psr_code = third_psr.requestPsrThirdApi(request_data)
    except AssertionError as err:
        return JsonResponse({'error':'报错信息{0}'.format(err)})

    try:
        # 更改生成的调拨单状态
        psr_codes = PsrMessage().updatePsrBstatusByCode(result_psr_code)
        print('oa创建成功，且修改调拨请求的bstatus状态')
        # wsp创建调拨请求与包裹单
        put_wsp_db = CreateWspPSR().psr_create_pck([psr_codes])
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
    try:
        wms_code = isr.createIsrRequestToWms(post.get('sft_code'))
    except AssertionError as  err:
        return JsonResponse({'报错提示': '{0}'.format(err).replace('\\', '')})

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
    post_data['originProcessCenterId'] = post.get('ProcessCenterId')
    post_data['targetProcessCenterId'] = post.get('ProcessCenterId')
    # find_goods_code = goodsSql()
    wsp_db =InstorageMessage()
    post_data['baseProductCode'] = post.get('goods_code')
    start_code = post_data['baseProductCode'][0:3].upper()
    #WSP创建调拨单接口，如果判断property_id与productId都为空，则用baseProductCode查询goods表获取产品信息
    post_data['propertyId'] = None
    post_data['productId'] = None
    if start_code!="PBU":
        try:
            base_product_code = wsp_db.findGoodsInfo( post_data['baseProductCode'])
        except TypeError:
            print('产品信息为空')
            return JsonResponse({'error_message': '产品信息为空'})
        post_data['baseProductCode'] = base_product_code

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
    wsp_codes = isr.syncFromProductShiftInfo(create_info)
    wms_codes = isr.isrFromWspToWms(wsp_codes)
    return JsonResponse({'wms_code': wms_codes})

@csrf_exempt
def InStorageRequestPPL(request):
    """
    生成入库申请
    :param request:
    :return:
    """
    post = request.POST
    if post.__len__() == 0:
        post = json.loads(request.body)
    post_data = {}
    post_data['ppl_code'] = post.get('ppl_code')
    isr = CreatePPLInstorageRequest()
    wms_code = isr.createIsrRequestToWms(post.get('ppl_code'),post.get('is_wms'))
    print('创建入库单成功的单据{0}'.format(wms_code))
    return JsonResponse({'wms_code': list(wms_code)})

@csrf_exempt
def virtualInstorageRequestPPL(request):
    ppl_list = request.POST
    if ppl_list.__len__() == 0:
        ppl_list = json.loads(request.body)
    nowDate = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    zzl_user_id = 50561
    ppl_instorages = []
    ppl_instorage = {}
    ppl_instorage['originProcessCenterId'] = ppl_list['OriginProcessCenterId']
    ppl_instorage['targetProcessCenterId'] = ppl_list['TargetProcessCenterId']
    ppl_instorage['shipType'] = ppl_list['shipType']
    ppl_instorage['lastUpdateTime'] = nowDate
    ppl_instorage['lastUpdateUserId'] = zzl_user_id
    ppl_instorage['createUserId'] = zzl_user_id
    ppl_instorage['createTime'] = nowDate
    ppl_instorage['quantity'] = ppl_list['quantity']
    wsp_db =InstorageMessage()
    try:
        porduct_info = wsp_db.findGoodsOAId( ppl_list['goods_code'])
    except TypeError:
        print('产品信息为空')
        return JsonResponse({'error_message': 'goods,goods_bar_code与goods_mapper_bg_product联表查询产品信息为空'})

    ppl_instorage['productId'] = porduct_info['bg_product_id']
    ppl_instorage['propertyId'] = porduct_info['bg_property_id']
    ppl_instorage['isTest'] = ppl_list['isTest'] #是否需求测试
    ppl_instorage['goodsType'] = ppl_list['goodsType']
    ppl_instorage['vacuumPacking'] = 0  #是否真空包装
    ppl_instorage['isShiftCosting'] = 0  #'是否资本化[0-来源仓入库结算,1-目标仓入库结算]',
    ppl_instorage['goodsSize'] = 0   #o：普通 1：大货
    ppl_instorage['salePlatform'] = 0  # 销售平台',
    # ppl_instorage['packageId'] = ppl_list['PackageID']
    ppl_instorage['packageCode'] = GetCode().getPPLCode(1)[0]
    # lclLimitLevel 在原代码中是判断货物类型为21的则不允许拼箱，不为21允许相同货主拼箱
    ppl_instorage['lclLimitLevel'] = "允许相同货主拼箱"
    ppl_instorage['storageCode'] = 0  #仓库代码
    ppl_instorage['amazonShop'] = 0    # '亚马逊店铺',
    ppl_instorage['deliveryProductCode'] = ''  #分箱子明细发货条码
    ppl_instorage['isDrowback'] = 0  #是否退税
    ppl_instorage['shipmentId'] = ''   #入库单号
    ppl_instorages.append(ppl_instorage)
    isr = CreatePPLInstorageRequest()
    #生成源单与作业单据
    wsp_codes = isr.syncFromPPL(ppl_instorages)
    #下发到wms
    wms_code = isr.isrFromWspToWms(wsp_codes)
    return JsonResponse({'wms_code':wms_code})


@csrf_exempt
def virtualSyncSFT(request):
    sft_list = request.POST
    if sft_list.__len__() == 0:
        sft_list = json.loads(request.body)
    now_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    source_process_id = sft_list['source_process_id']
    targer_process_id = sft_list['targer_process_id']
    goods_type = sft_list['goods_type']
    shifs_type = sft_list['shiftType']
    # 接口参数汇总
    sft_request_list = []
    #主表调拨单信息
    sft_request = {}
    sft_request['modifyTimeStamp'] = now_date
    sft_request['modifyDate'] = now_date
    get_code=GetCode()
    sft_code = get_code.getOaSFTCode(1)[0]
    sft_request['productShiftItemCode'] =  sft_code
    sft_request['originProcessCenterId'] =  source_process_id
    sft_request['targetProcessCenterId'] =  targer_process_id
    sft_request['shipType'] = shifs_type
    sft_request['goodsType'] =  goods_type
    sft_request['lastTraceStatus'] =  0
    sft_request['modifyUserId'] =  0
    sft_request['modifyUserName'] =  ""
    sft_request['goodsSize'] =  0
    sft_request['productShiftOriginCode'] =  ""
    productShiftBoxList = []
    sft_request['productShiftBoxList'] = productShiftBoxList
    sft_request_list.append(sft_request)
    #分箱信息
    request_box_info_lists = sft_list['box_lists']
    find_goods_code = goodsSql()
    zzl_user_id = 50561
    # 需要分箱数
    box_num = 0
    for i in request_box_info_lists:
        box_num += int(i['box_num'])
    #箱号列表
    box_code_list = get_code.getOaBoxCode(box_num)
    psr_code = PsrMessage().getPsrCodeByGoodsType(goods_type)
    count = 0
    for index,box_code_info in enumerate(request_box_info_lists):
        sft_request_box={}
        sft_request_box['originProcessCenterId'] =  source_process_id
        sft_request_box['targetProcessCenterId'] =  targer_process_id
        sft_request_box['shipType'] =  shifs_type
        sft_request_box['goodsType'] =  goods_type
        sft_request_box['length'] =  1000
        sft_request_box['height'] =  900
        sft_request_box['width'] =  900
        sft_request_box['weight'] =  15
        sft_request_box['userId'] =  zzl_user_id
        sft_request_box['modifyTimeStamp'] =  None
        sft_request_box['ful'] =  False
        sft_request_box['boxDeleted'] =  False
        #分箱明细
        productShiftBoxItemList = []
        sft_request_box['productShiftBoxItemList'] = productShiftBoxItemList
        goods_infos = box_code_info['goods_info']
        for goods_info in goods_infos:
            sft_request_box_item={}
            goods_code = goods_info['goods_code']
            goods_message={}
            if goods_code[0:3].upper() == "POA":
                poa_code = goods_code
                try:
                    goods_message = find_goods_code.findOaGoodsByPoa(poa_code)
                    sft_request_box_item['propertyId'] = goods_message['poa_id']
                    sft_request_box_item['productId'] = goods_message['sku_id']
                except TypeError:
                    print('产品信息为空')
            else:
                sft_request_box_item['productId'] = find_goods_code.findOaGoodsBySku(goods_code)
                sft_request_box_item['propertyId'] = 0
            box_code_list.append(sft_request_box)
            sft_request_box_item['originCode'] = psr_code
            sft_request_box_item['quantity'] = goods_info['product_num']
            # sft_request_box_item['propertyId'] = False

            sft_request_box_item['amazonShop'] = "amazonShopApi"
            productShiftBoxItemList.append(sft_request_box_item)
        for i in range(0,box_code_info['box_num']):
            sft_request_box_copy =  copy.deepcopy(sft_request_box)
            sft_request_box_copy['productShiftBoxCode'] = box_code_list[count]
            count += 1
            productShiftBoxList.append(sft_request_box_copy)

    request_data = json.dumps(sft_request_list,cls=DateEncoder)
    SftFlow().createOaSFT(request_data)
    print(request_data)
    # return JsonResponse(request_data,safe=False,json_dumps_params={'ensure_ascii':False})
    return JsonResponse({"sft_code":sft_code,"box_code":box_code_list},safe=False,json_dumps_params={'ensure_ascii':False})


    pass

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



