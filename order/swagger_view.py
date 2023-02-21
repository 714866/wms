from django.http import JsonResponse
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from rest_framework.decorators import action
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView

from .serializers import MqOrderCreateSerializer


class MqOrder(APIView):
    '''发送mq信息，创建订单信息的'''
    # 不指定序列化值，会报错： unable to guess serializer. This is graceful fallback handling for APIViews. Consider using GenericAPIView as view base class, if view is under your control. Ignoring view for now.
    serializer_class = MqOrderCreateSerializer
    @extend_schema(description='mq创建订单',operation_id='23',
                   methods=["POST"],
                   parameters=[


                       OpenApiParameter(name='body',examples=[OpenApiExample('Example input',
            description='Creation of an alias',
            value={
                'user_id': 1234567890,
                'obj_id': 288,
                'alias': 'my alias'
            })], ),
                   ],
                   request=MqOrderCreateSerializer


                   )
    @action(detail=True, methods=['post'])
    def post(self,request):

        return JsonResponse({'statue':200})




