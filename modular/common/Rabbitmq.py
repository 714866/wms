import json
import pika
import datetime


# 生成消息入口处
def get_message():
    for i in range(10):  # 生成10条消息
        message = json.dumps(
            {
                "haikwanDatas": [
                    {
                        "orderId": "A0003623011000GE",
                        "sku": "SKUI98667",
                        "poa": None,
                        "enName": "Paddle protector base",
                        "cnName": "桨保护器底座",
                        "quantity": 1,
                        "producingArea": "CN",
                        "weight": 0,
                        "currency": "USD",
                        "hscode": "9503009000",
                        "balance": "1.0500",
                        "itemIndex": "0",
                        "realPrice": "3.5000",
                        "batteryType": 0
                    }
                ],
                "orderData": {
                    "id": "6343cc1218a0742618134463",
                    "packageId": "PCK0934221010DX622",
                    "orderId": "A0003623011000GE",
                    "oaOrderStatus": "3",
                    "platformName": "Banggood",
                    "platformNo": 1,
                    "shops": "banggoodsz",
                    "outsideId": "",
                    "shopId": 2558,
                    "productManagerId": 60607,
                    "salesUserId": 9983,
                    "shipworksorder": "110702451",
                    "orderInfoJson": None,
                    "trackingType": 0,
                    "orderTypes": "normal",
                    "importDateTime": "2022-10-10 15:38:41",
                    "operateDateTime": "2022-10-10 15:38:58",
                    "payTime": "2022-10-10 23:37:18",
                    "orginalOrderTime": "2022-10-10 23:36:46",
                    "confirmedTime": "2022-10-10 15:38:57",
                    "userTraceId": "",
                    "confirmedTimeStamp": "1665416337000",
                    "deliverGoodsId": "1665416337000",
                    "paymentType": 1,
                    "ppNote": "",
                    "orderRemark": "",
                    "errorCode": "",
                    "isUnsalable": 0,
                    "logisticsAccount": "00036",
                    "freightCarrier": 0,
                    "parentOaOrderIds": None,
                    "orderDeliveryPriority": 0,
                    "modifyDate": "2022-10-10 15:38:57",
                    "setting": "",
                    "recipient": "Chris Berthold",
                    "phone": "0414787945",
                    "email": "sunbeam61@tpg.com.au",
                    "zipCode": "2617",
                    "regionId": "7018356860371809634",
                    "areaId": "3473740288318517555",
                    "countryCode": "AU",
                    "countryName": "澳大利亚",
                    "country": "AUSTRALIA",
                    "countryId": "13",
                    "processCenterId": 1150,
                    "state": "Australian Capital Territory",
                    "city": "Evatt",
                    "address1": "30 Callaghan Str",
                    "address2": "",
                    "address": "30 Callaghan Str\n  Evatt\n  Australian Capital Territory\n  2617",
                    "masterMailing": "2086",
                    "transportLevelId": 5697,
                    "postTypeOptions": "2086|0,2032|0,2143|0",
                    "predictionTraceId": None,
                    "predictionlabel": None,
                    "predictionPostId": None,
                    "shippingService": "Standard Shipping",
                    "weightLevel": 0,
                    "totalPrice": 18.07,
                    "originalTotalFee": 28.19,
                    "originalCurrency": "AUD",
                    "originalAmount": 23.53,
                    "originalShipFee": 4.66,
                    "wetherlossable": False,
                    "lossableAmount": None,
                    "maximumCost": 228.3381,
                    "bargainInterceptionType": 1,
                    "throwingGoodsSent": 0,
                    "lossInterceptTypeLog": "产品成本+运费-1.00*订单总价值&gt;100.00元（人民币）",
                    "preSendTime": "2022-10-12 02:37:18",
                    "haikwanDetails": None,
                    "orderDetails": None,
                    "customerOrderType": "",
                    "iossNumber": "IM1010000003",
                    "recipientInfoDecryptionCode": None,
                    "createTime": "2022-10-10 15:38:58",
                    "buyerDistrict": "",
                    "totalPriceWithoutTax": "16.4300",
                    "customerPayTax": "0",
                    "recipientHouseNumber": "",
                    "nationalIdNumber": "",
                    "jumpMainPost": False,
                    "repeatSend": False,
                    "megerOrder": False,
                    "replenishment": False,
                    "changeMark": False,
                    "split": False
                },
                "orderDetailDatas": [
                    {
                        "orderId": "A0003623011000GE",
                        "orderDetailId": 678330037,
                        "itemId": "1611001",
                        "transactionId": 0,
                        "originalitemCode": "2xSKUD85866",
                        "originalQuantity": "1",
                        "url": "https://www.banggood.com/2pcs-Eachine-Mini-Mustang-P-51D-Mini-F4U-T-28-Trojan-F16-F22-BF109-Spitfire-P40-RC-Airplane-Spare-Part-Propeller-Protector-Mount-p-1611001.html",
                        "orderDetailInfoJson": "{\"originalQuantity\":\"1\",\"originalitemCode\":\"2xSKUD85866\",\"url\":\"https://www.banggood.com/2pcs-Eachine-Mini-Mustang-P-51D-Mini-F4U-T-28-Trojan-F16-F22-BF109-Spitfire-P40-RC-Airplane-Spare-Part-Propeller-Protector-Mount-p-1611001.html\"}",
                        "sku": "SKUI98667",
                        "poa": None,
                        "quantity": 1,
                        "itemEnName": "[SKUI98667]2pcs Eachine Mini Mustang P-51D Mini F4U T-28 Trojan F16 F22 BF109 Spitfire P40 RC Airplane Spare Part Propeller Protector Mount[+Type;2 pairs]",
                        "itemName": "2pcs Eachine Mini Mustang P-51D小固定翼桨保护器底座 带桨保护器版2个",
                        "colorSel": "",
                        "productId": "26335440",
                        "propertyId": "0",
                        "productWeight": 12,
                        "propertyWeight": 0,
                        "productReWeight": 5,
                        "propertyReWeight": 0,
                        "salesStatus": 0,
                        "volumeLength": 8,
                        "volumeWidth": 6,
                        "volumeHeight": 2,
                        "packageLength": 8,
                        "packageWidth": 6,
                        "packageHeight": 2,
                        "barCode": "",
                        "salePrice": 3.5,
                        "productLabels": [
                            "24",
                            "147",
                            "164",
                            "216",
                            "247",
                            "266",
                            "268",
                            "274",
                            "277"
                        ],
                        "batteryType": 0,
                        "discountPrice": 0,
                        "costPrice": 3,
                        "averageTransferCost": 0,
                        "avgWareHousingCostPrice": 0,
                        "vatCost": 0,
                        "categoryForAe": {
                            "categoryId": "790505",
                            "categoryIdPath": "|79|7905|790505|",
                            "cnName": "固定翼",
                            "cnNamePath": "玩具类 &gt; 遥控主机玩具 &gt; 固定翼",
                            "enName": "Remote Control Airplane",
                            "enNamePath": "Toy &gt; Remote Control Toys &gt; Remote Control Airplane",
                            "strCategoryId": "790505"
                        },
                        "platformCategoryId": "",
                        "os_Detail_ID": 166867594,
                        "productGroup": False,
                        "gift": False,
                        "stockShip": False,
                        "canSplit": False
                    }
                ]
            }
        )
        producter(message)


# 消息生产者

def producter(message):  # 消息生产者
    # 获取与rabbitmq 服务的连接，虚拟队列需要指定参数 virtual_host，如果是默认的可以不填（默认为/)，也可以自己创建一个
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='192.168.1.146', port=5672, credentials=pika.PlainCredentials('guest', 'guest'),virtual_host='sp-crm'))
    # 创建一个 AMQP 信道（Channel）,建造一个大邮箱，隶属于这家邮局的邮箱
    channel = connection.channel()
    # 声明消息队列tester，消息将在这个队列传递，如不存在，则创建,durable参数与mq配置的要一样，且
    channel.queue_declare(queue='q_ewms_wosPrep_flow_handle',durable=True)
    # 向队列插入数值 routing_key的队列名为tester，body 就是放入的消息内容，exchange指定消息在哪个队列传递，这里是空的exchange但仍然能够发送消息到队列中，因为我们使用的是我们定义的空字符串“”exchange（默认的exchange）
    channel.basic_publish(exchange='x_sp_orderservice', routing_key='r_order_orderservice_flow_push_autoconfirminfo', body=message)
    # 关闭连接
    connection.close()


if __name__ == "__main__":
    
    get_message()  # 程序执行入口