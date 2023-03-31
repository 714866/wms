from django.db import connections
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.views import APIView

from modular.common.comm_decorator import catch_exception
from modular.common.commonDB import wms_sql_select_return_dict
from modular.common.craetecode import GetCode
from modular.common.wmsRequests import wmsRequest
from .commSql.instorage_sql import find_instorage_code_by_relatedcode, find_receipt_code, find_shelf_by_source_code
from .models import OdsPckInfo, OdsPckDetail, OdsPckAttached, OdsPckHaikwanDetail, Receipt,Shelf
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
    @extend_schema(description='手持PDA入库',methods=['GET'],
                   parameters=[OpenApiParameter(name='code',description='入库单据',required=True)],
                   )
    def get(self,request):
        code = request.query_params.get('code')
        if code.upper().startswith('IHP') or code.upper().startswith('RC'):
            info = Receipt.objects.filter(Q(source_code=code)|Q(receipt_code=code)).first()
        else:
            info = wms_sql_select_return_dict(find_receipt_code(code))

        response = wmsRequest().save_instorage(info)
        return JsonResponse(response)


class PdaUpdateShelfRack(APIView):
    """
    手持上架 ，上架单号与来源单号不能同时为空
    """
    @extend_schema(description='手持上架',methods=['GET'],
                   parameters=[OpenApiParameter(name='shelfCode',description='上架单号',required=False),
                               OpenApiParameter(name='sourceCode',description='来源单号',required=False),
                               OpenApiParameter(name='rack',description='上架货位',required=True,),
                               OpenApiParameter(name='quantity',description='上架数量-不填写默认全部',required=False,)
                               ])
    def get(self,request):
        source_code = request.query_params.get('sourceCode')
        shelf_code = request.query_params.get('shelfCode')
        if source_code is None and shelf_code is None:
            return JsonResponse({"error": 'shelf_code与scam_code不能同事为空'})

        shelf_api_info_list=[]
        if shelf_code:
            update_shelf_info = Shelf.objects.values("goods_id","quantity","source_code","shelf_code","in_quantity","exception_quantity").filter(shelf_code=shelf_code).first()
            if update_shelf_info is None:
                return JsonResponse({"error": '上架单{0}不存在'.format(shelf_code)})
            update_shelf_info['rack'] = request.query_params.get('rack')
            update_shelf_info['quantity'] = request.query_params.get('quantity') if request.query_params.get('quantity')  else (update_shelf_info['quantity']-update_shelf_info.get('in_quantity')-update_shelf_info.get('exception_quantity'))
            response = wmsRequest().update_shelf_rack([update_shelf_info])
            print('查找shelf表数据，获取goodsId，数量quantity')
        else:
            shelf_info_list = wms_sql_select_return_dict(find_shelf_by_source_code(source_code,request.query_params.get('rack')))
            print('通过来源单号来实现上架')
            response = wmsRequest().update_shelf_rack(shelf_info_list)
        return JsonResponse(response)

class TwmsOdsPckInfo(APIView):
    @extend_schema(description='查询twms包裹单的')
    def post(self, request):
        # GetCode().get_twms_pck_code(1038)
        OdsPckInfo.objects.using('twms').create(id=get_snow_id(),
                                                order_id='',
                                                package_id='',
                                                )
