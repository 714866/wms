from django.http import JsonResponse
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from rest_framework.decorators import action
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView

from modular.common.Rabbitmq import order_producter
from modular.common.craetecode import get_order_codes
from modular.goods.wsp_goods import WspGoods
from modular.order.mqMessages import get_order_mq_message
from wmspda.models import OdsPckInfo
from .serializers import MqOrderCreateSerializer, OrderSerializer


class MqOrder(APIView):
    '''发送mq信息，创建订单信息的'''
    # 不指定序列化值，会报错： unable to guess serializer. This is graceful fallback handling for APIViews. Consider using GenericAPIView as view base class, if view is under your control. Ignoring view for now.
    serializer_class = OrderSerializer
    @extend_schema(description='mq创建订单',summary='mq创建订单',operation_id='23',
                   methods=["POST"],
            # 设置请求例子
            #        parameters=[
            #            OpenApiParameter(name='body',examples=[OpenApiExample('Example input',
            # description='Creation of an alias',
            # value={
            #     'user_id': 1234567890,
            #     'obj_id': 288,
            #     'alias': 'my alias'
            # })], ),
            #        ],
                   request={"application/json":MqOrderCreateSerializer}
                   # request=MqOrderCreateSerializer


                   )
    @action(detail=True, methods=['post'])
    def post(self,request):
        data = request.data
        product_info_list = []
        wsp_db = WspGoods()
        for product_info in data['productLists']:
            #处理产品信息，需要sku,poa，与对应oaid
            order_goods_infos = wsp_db.find_goods_by_order_info(product_info['product_code'])
            order_goods_infos['product_num']=product_info['product_num']
            product_info_list.append(order_goods_infos)
        # 获取A单号
        order_code_list = get_order_codes(data['order_num'])
        for i in range(data['order_num']):
            # 组成参数
            mq_message = get_order_mq_message(data['process_center'],product_info_list,order_code_list[i])
            #发送消息
            order_producter(mq_message)

        #订单生成为异步的，所以存在时间差，统一在调用mq后，再查数据是否生成
        result_order = []
        for i in range(data['order_num']):
            infor = wsp_db.cursor.fetchone("select id from ods_pck_info where order_id='{0}'".format(order_code_list[i]))
            if infor is not None:
                result_order.append(order_code_list[i])
        return JsonResponse({'statue':200,'success_order_id':result_order,'put_order_id':order_code_list})




