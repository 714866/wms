import time

from modular.common.craetecode import get_order_codes


def get_order_mq_message(process_id, product_lists, order_id,shop_id=1223):
    """

    :param process_id: 订单处理中心
    :param product_lists:  产品列表
    :return:
    """
# 渠道2123   2129是物流那边通用能返回面单的渠道

    haikwan_datas = []
    order_detail_datas = []
    for index, product_list in enumerate(product_lists):
        haikwan_dict = {
            # "orderId": "A0003623011000GE",
            "orderId": order_id,
            "sku": product_list.get('bg_product_code'),
            "poa": product_list.get('bg_property_code'),
            "enName": "xxx",
            "cnName": "xxx",
            "quantity": 1,
            "producingArea": "CN",
            "weight": 0,
            "currency": "USD",
            "hscode": "9503009000",
            "balance": "1.0500",
            "itemIndex": index,
            "realPrice": "3.5000",
            "batteryType": 0
        }
        haikwan_datas.append(haikwan_dict)

        order_detail_dict = {

            "orderId": order_id,
            "orderDetailId": 678330037,
            "itemId": "1611001",
            "transactionId": 0,
            "originalitemCode": product_list.get('bg_product_code'),
            "originalQuantity": product_list.get('product_num'),
            "url": "https://www.banggood.com/2pcs-Eachine-Mini-Mustang-P-51D-Mini-F4U-T-28-Trojan-F16-F22-BF109-Spitfire-P40-RC-Airplane-Spare-Part-Propeller-Protector-Mount-p-1611001.html",
            "orderDetailInfoJson": "{\"originalQuantity\":\""+str(product_list.get('product_num'))+"\",\"originalitemCode\":\""+product_list.get('bg_product_code')+"\",\"url\":\"https://www.banggood.com/2pcs-Eachine-Mini-Mustang-P-51D-Mini-F4U-T-28-Trojan-F16-F22-BF109-Spitfire-P40-RC-Airplane-Spare-Part-Propeller-Protector-Mount-p-1611001.html\"}",
            "sku": product_list.get('bg_product_code'),
            "poa": product_list.get('bg_property_code'),
            "quantity": product_list.get('product_num'),
            "itemEnName": "xxx",
            "itemName": "xxx",
            "colorSel": "",
            "productId": product_list.get('bg_product_id'),
            "propertyId":product_list.get('bg_property_id'),
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
            "barCode": "barCode",   #三方编码
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
                "cnName": "xxx",
                "cnNamePath": "xxx",
                "enName": "xxx",
                "enNamePath": "xxx",
                "strCategoryId": "790505"
            },
            "platformCategoryId": "",
            "os_Detail_ID": 166867594,
            "productGroup": False,
            "gift": False,
            "stockShip": False,
            "canSplit": False
        }
        order_detail_datas.append(order_detail_dict)
    order_data = {
        "id": "6343cc1218a0742618134463",
        "orderId": order_id,
        "oaOrderStatus": "3",
        "platformName": "Banggood",
        "platformNo": 1,
        "shops": "banggoodsz",
        "outsideId": "",
        "shopId": shop_id,  #店铺id
        "productManagerId": 60607,
        "salesUserId": 9983,
        "shipworksorder": "110702451",
        "orderInfoJson": None,
        "trackingType": 0,
        "orderTypes": "normal",
        "importDateTime": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),
        "operateDateTime": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),
        "payTime": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),
        "orginalOrderTime": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),
        "confirmedTime": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),
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
        "modifyDate": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),
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
        "processCenterId": process_id,
        "state": "Australian Capital Territory",
        "city": "Evatt",
        "address1": "30 Callaghan Str",
        "address2": "",
        "address": "30 Callaghan Str\n  Evatt\n  Australian Capital Territory\n  2617",
        "masterMailing": "2123",  #  渠道id
        "transportLevelId": 5697,
        "postTypeOptions": "2123|0",  # 渠道id
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
        # "preSendTime": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), 小写%Y，最后结果年份是23 两位数
        "preSendTime": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),
        "haikwanDetails": None,
        "orderDetails": None,
        "customerOrderType": "",
        "iossNumber": "IM1010000003",
        "recipientInfoDecryptionCode": None,
        "createTime": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),
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
    }


    order_message = {'haikwanDatas': haikwan_datas, 'orderData': order_data, 'orderDetailDatas': order_detail_datas}

    print(order_message)
    return order_message



if __name__=='__main__':
    from modular.common.Rabbitmq import order_producter
    from modular.goods.wsp_goods import WspGoods

    wsp_db = WspGoods()
    order_code_list = get_order_codes(1)
    order_goods_infos = wsp_db.find_goods_by_order_info('POA1308097')
    order_goods_infos['product_num'] = 2
    mq_message = get_order_mq_message(1087, [order_goods_infos], order_code_list[0],shop_id=542)
    # 发送消息
    order_producter(mq_message)