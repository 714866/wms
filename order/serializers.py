from rest_framework import serializers

class ProductListField(serializers.Serializer):
    product_code = serializers.CharField()
    product_num = serializers.IntegerField()

class MqOrderCreateSerializer(serializers.Serializer):
    # 声明序列化器
    # 1. 字段声明[ 要转换的字段，当然，如果写了第二部分代码，有时候也可以不用写字段声明 ]
    process_center = serializers.CharField(default=1138)
    order_num = serializers.IntegerField(default=1)

    # ggg = serializers.ListField(source='ProductListField')
    productLists = ProductListField(many=True)

class OrderSerializer(serializers.Serializer):
    pass