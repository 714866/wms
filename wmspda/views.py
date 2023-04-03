import json
import time

from django.db.models import Q
from django.http import JsonResponse

# Create your views here.
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.views import APIView

from modular.SFT.createSftInstorageRequest import CreateSfiInstorageRequest
from modular.common.comm_decorator import catch_exception
from modular.common.commonDB import wms_sql_select_return_dict
from modular.common.craetecode import GetCode
from modular.common.wmsRequests import wmsRequest
from modular.goods.wms_goods import WmsGoods
from modular.wspDB.instoragerequest import InstorageMessage
from .commSql.instorage_sql import find_instorage_code_by_relatedcode, find_receipt_code, find_shelf_by_source_code
from .models import OdsPckInfo, OdsPckDetail, OdsPckAttached, OdsPckHaikwanDetail, Receipt, Shelf, Goods
from modular.common.snowID import get_snow_id


class PdaLogin(APIView):
    '''
    post:
    手持登录接口
    '''

    @extend_schema(description='模拟页面普通创建PSR接口',
                   methods=["POST"],
                   parameters=[
                       OpenApiParameter(name='username', description='用户名', type=str,
                                        default='zhuzhiliang@banggood.com'),
                       OpenApiParameter(name='password', description='密码', default='123456', type=str)
                   ]
                   )
    def post(self, request):
        login_url = 'http://172.16.6.203:18201/own-wms-api/pda/sys-user/login'
        api_params = request.query_params
        use = OdsPckInfo.objects.filter(order_id='A0005121030402RX')
        use1 = OdsPckInfo.objects.using('twms').filter(order_id='A0005121030402RX')
        r = wmsRequest(is_login=False)
        r.login(api_params)


class PdaSaveShelf(APIView):
    '''
    post:
    手持入库签收接口
    '''

    @extend_schema(description='手持PDA入库签收',
                   methods=["GET"],
                   parameters=[
                       OpenApiParameter(name='targetCode', description='入库签收单据', type=str
                                        ),
                   ]
                   )
    def get(self, request):
        target_code = request.query_params.get('targetCode')
        api_action = wmsRequest()
        result = api_action.save_shelf(target_code)
        # return JsonResponse({'psr':'PPL-20220819-610852' })
        return JsonResponse(result)


class PdaSaveReceipt(APIView):
    """
    手持收货
    """

    # @catch_exception 自写装饰器在上面的时候，extend_schema没生效
    @extend_schema(description='手持PDA收货', methods=["GET"],
                   parameters=[OpenApiParameter(name='code', description='收货单据', required=True), ], )
    # @catch_exception
    def get(self, request):
        # return result
        info = wms_sql_select_return_dict(find_instorage_code_by_relatedcode(request.query_params.get('code')))

        response = wmsRequest().save_receipt(info)
        return JsonResponse(response)


class PdaSaveInStorage(APIView):
    """
    手持入库
    """

    @extend_schema(description='手持PDA入库', methods=['GET'],
                   parameters=[OpenApiParameter(name='code', description='入库单据', required=True)],
                   )
    def get(self, request):
        code = request.query_params.get('code')
        if code.upper().startswith('IHP') or code.upper().startswith('RC'):
            info = Receipt.objects.filter(Q(source_code=code) | Q(receipt_code=code)).first().receipt_code
        else:
            info = wms_sql_select_return_dict(find_receipt_code(code))['receipt_code']

        response = wmsRequest().save_instorage(info)
        return JsonResponse(response)


class PdaUpdateShelfRack(APIView):
    """
    手持上架 ，上架单号与来源单号不能同时为空
    """

    @extend_schema(description='手持上架', methods=['GET'],
                   parameters=[OpenApiParameter(name='shelfCode', description='上架单号', required=False),
                               OpenApiParameter(name='sourceCode', description='来源单号', required=False),
                               OpenApiParameter(name='rack', description='上架货位', required=True, ),
                               OpenApiParameter(name='quantity', description='上架数量-不填写默认全部', required=False, )
                               ])
    def get(self, request):
        source_code = request.query_params.get('sourceCode')
        shelf_code = request.query_params.get('shelfCode')
        if source_code is None and shelf_code is None:
            return JsonResponse({"error": 'shelf_code与scam_code不能同事为空'})
        # 上架单传参参数列表
        shelf_info_list = []
        if shelf_code:
            update_shelf_info = Shelf.objects.values("goods_id", "quantity", "source_code", "shelf_code", "in_quantity",
                                                     "exception_quantity").filter(shelf_code=shelf_code).first()
            if update_shelf_info is None:
                return JsonResponse({"error": '上架单{0}不存在'.format(shelf_code)})
            update_shelf_info['rack'] = request.query_params.get('rack')
            update_shelf_info['quantity'] = request.query_params.get('quantity') if request.query_params.get(
                'quantity') else (
                        update_shelf_info['quantity'] - update_shelf_info.get('in_quantity') - update_shelf_info.get(
                    'exception_quantity'))
            shelf_info_list.append(update_shelf_info)
            response = wmsRequest().update_shelf_rack(shelf_info_list)
            print('查找shelf表数据，获取goodsId，数量quantity')
        else:
            shelf_info_list = wms_sql_select_return_dict(
                find_shelf_by_source_code(source_code, request.query_params.get('rack')))
            if len(shelf_info_list) == 0:
                return JsonResponse({'error': ''})
            print('通过来源单号来实现上架')
            response = wmsRequest().update_shelf_rack(shelf_info_list)
        return JsonResponse(response)


class goodsShelf(APIView):

    @extend_schema(description='按产品货位完成上架', methods=['GET'],
                   parameters=[OpenApiParameter(name='goodsCode', description='产品', required=True,),
                               OpenApiParameter(name='quantity', description='数量', required=True),
                               OpenApiParameter(name='rack', description='上架货位', required=True),
                               OpenApiParameter(name='processcenter', description='上架处理中心', required=True)
                               ])
    def get(self, request):
        # 1.生成调拨的入库申请单

        post_datas = []
        post_data = {}
        post_data['quantity'] = request.query_params.get('quantity')
        post_data['originProcessCenterId'] = request.query_params.get('processcenter')
        post_data['targetProcessCenterId'] = request.query_params.get('processcenter')
        # find_goods_code = goodsSql()

        wsp_db = InstorageMessage()
        post_data['baseProductCode'] = request.query_params.get('goodsCode')
        start_code = post_data['baseProductCode'][0:3].upper()
        # WSP创建调拨单接口，如果判断property_id与productId都为空，则用baseProductCode查询goods表获取产品信息
        post_data['propertyId'] = None
        post_data['productId'] = None
        if start_code != "PBU":
            try:
                base_product_code = wsp_db.findGoodsInfo(post_data['baseProductCode'])
            except TypeError:
                print('wsp产品信息为空')
                return JsonResponse({'error_message': 'wsp产品{0}信息为空'.format(post_data['baseProductCode'])})
            post_data['baseProductCode'] = base_product_code

        now_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        post_data['modifyTimeStamp'] = now_date

        # 自建单号SFT-T1-日期 ,暂时只做单条的逻辑
        get_code = GetCode()
        sft_codes = get_code.getSftCode(1)
        post_data['originCode'] = sft_codes[0]
        box_codes = get_code.getboxCode(1)
        post_data['productShiftBoxCode'] = box_codes[0]
        post_data['productShitItemOriginCode'] = ''
        post_data['shipType'] = 'General'
        post_data['goodsType'] = 0
        post_data['length'] = '120'
        post_data['width'] = '120'
        post_data['height'] = '120'
        post_data['weight'] = '120'
        post_data['storageCode'] = ''
        post_data['deliveryProductCode'] = ''
        post_data['amazonShop'] = ''
        post_data['detailLabel'] = ''
        post_data['relativeCode'] = ''
        post_data['traceCode'] = ''
        post_data['logId'] = ''
        post_data['goodsSize'] = ''
        post_data['fboxItemOriginCode'] = ''
        post_data['type'] = ''
        post_data['ful'] = False
        post_datas.append(post_data)
        isr = CreateSfiInstorageRequest()
        # 组装参数
        create_info = isr.wspApiMessages(post_datas)
        wsp_codes = isr.syncFromProductShiftInfo(create_info)
        wms_codes = isr.isrFromWspToWms(wsp_codes)

        #需要增加对产品是否在wms的判断
        wms_goods_info = Goods.objects.values('id').filter(base_product_code=request.query_params.get('goodsCode')).first()
        if wms_goods_info is None:
            #从wsp拉数据到wms
            wms_goods = WmsGoods()
            wms_goods.inser_goods_from_wsp_by_goods_code(request.query_params.get('goodsCode'))
            wms_goods.fix_goods_weigth_and_volume(sft_codes[0])

            pass
        # 2.进行入库签收
        wms_request = wmsRequest()
        wms_request.update_user_processcenter(request.query_params.get('ProcessCenterId'))
        save_shelf_response = wmsRequest().save_shelf(wms_codes[0])
        if save_shelf_response.get('error'):
            #返回入库
            return save_shelf_response

        # 3进行上架
        #todo 后期需加收对货位是否可用的判断
        shelf_info_list = wms_sql_select_return_dict(
            find_shelf_by_source_code(wms_codes[0], request.query_params.get('rack')))
        if len(shelf_info_list) == 0:
            return JsonResponse({'error': '{code}未生成上架单'.format(code=wms_codes[0])})

        response = wmsRequest().update_shelf_rack(shelf_info_list)
        if json.loads(response.text)['errorInfos'] is not None:
            # 判断是否有报错信息
            return {"error": True, "error_info": json.loads(response.text)['errorInfos'][0]}
        return JsonResponse({'info': '{code}上架处理中心{process}到货架：{rack}，数量：{quantiy}成功'.format(
            code=wms_codes[0],process=request.query_params.get('processcenter'),quantiy=request.query_params.get('quantity'),
            rack=request.query_params.get('rack')
        )
        }
        )


class TwmsOdsPckInfo(APIView):
    @extend_schema(description='查询twms包裹单的')
    def post(self, request):
        # GetCode().get_twms_pck_code(1038)
        OdsPckInfo.objects.using('twms').create(id=get_snow_id(),
                                                order_id='',
                                                package_id='',
                                                )
