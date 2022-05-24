import requests
import simplejson as simplejson   # 解决数据库返回Decimal类型转换成json错误使用

from modular.SFT.enums.shiptype import ShipType
from modular.common.SqlChangeFormat import DateEncoder, SqlChangeFormat
from modular.oaDB.getSFT import SftMessage
import json

class CreateSfiInstorageRequest():
    def __init__(self):
        self.query_db = SftMessage()
        pass

    def oaNotMessageQueryProductShiftItemToWsp(self, separate_box_info_list):
        """
        预设给OA没sft也进行入库申请生成的方法
        :param separate_box_info_list:
        :return: 
        """
        pass
    def queryProductShiftItemToWsp(self,shif_codes):
        """
        替代同步系统的queryProductShiftItemToWsp接口，返回
        :param shif_codes:  调拨单号列表
        :return: 返回接口参数json
        """
        # sft_lists= self.query_db.getSFTtoInstorgeRequest(SqlChangeFormat.list_to_str(shif_codes))
        shif_codes = SqlChangeFormat.list_to_str(shif_codes)
        sft_lists= self.query_db.getSFTtoInstorgeRequest(shif_codes)
        product_shift_lists = []   #  # 存储 [{api_info},{api_info}]
        # product_shift_dicts = {}   #存放总调用字典数据  {sft_code:{api_info}}
        # product_shift_dict = {}  # 存放子调用字典数据{api_info}
        for sft_list in sft_lists:
            is_not_exit = True
            product_shift={}
            for p in  product_shift_lists:
                if sft_list['originCode']  == p['originCode']:
                    # 判断是否为重复的调拨单，sft_list以分箱为维度，存在一个调拨单多个分箱
                    is_not_exit=  False
                    product_shift=p
            if is_not_exit:
                ''' 不存在 证明主表信息没赋值，是新的调拨单'''
                # product_shift_dicts[sft_list['originCode']] = {}
                product_shift = {}
                product_shift['originCode']=  sft_list['originCode']
                product_shift['productShitItemOriginCode']=  sft_list['productShitItemOriginCode']
                product_shift['productShitItemOriginCode']=  sft_list['productShitItemOriginCode']
                product_shift['originProcessCenterId']=  sft_list['originProcessCenterId']
                product_shift['targetProcessCenterId']=  sft_list['targetProcessCenterId']
                product_shift['shipType'] =  ShipType[sft_list['shipType']].value
                product_shift['modifyTimeStamp'] =  sft_list['modifyTimeStamp']
                product_shift['goodsType'] =  sft_list['goodsType']
                product_shift['amazonShop'] =  sft_list['amazonShop']
                product_shift['storageCode'] =  sft_list['storageCode']
                product_shift['deliveryProductCode'] =  sft_list['deliveryProductCode']
                product_shift['relativeCode'] =  sft_list['relativeCode']
                product_shift['traceCode'] =  sft_list['traceCode']
                product_shift['goodsSize'] =  sft_list['goodsSize']
                product_shift['isCustoms'] = False  # 原逻辑是根据目标，来源处理中心与运输方式绝对是否需要报关字段，现在直接写死false
                product_shift['productShiftDownToWspItemList']=[]
                product_shift_lists.append(product_shift)  # 加到主表中

            productShiftDownToWspItemList=[]
            # 明细赋值

            item = {}
            item['baseProductCode'] = sft_list['baseProductCode']
            item['productId'] = sft_list['productId']
            item['propertyId'] = sft_list['propertyId']
            item['quantity'] = sft_list['quantity']
            item['height'] = sft_list['height']
            item['length'] = sft_list['length']
            item['width'] = sft_list['width']
            item['weight'] = sft_list['weight']
            item['productShiftBoxCode'] = sft_list['productShiftBoxCode']
            item['detailLabel'] = sft_list['detailLabel']
            item['ful'] = sft_list['ful']
            item['fboxItemOriginCode'] = sft_list['fboxItemOriginCode']
            item['type'] = sft_list['type']

            #请求参数组装明细

            product_shift['productShiftDownToWspItemList'].append(item)
            # product_shift_dict['originCode']['productShiftDownToWspItemList'].append(item)
            print(product_shift)

        product_shift_down_to_wsp_jsons=json.dumps(product_shift_lists,cls=DateEncoder)
        print(product_shift_down_to_wsp_jsons)
        return product_shift_down_to_wsp_jsons

    def syncFromProductShiftInfo(self,separate_box_info_list):

        pass



if __name__=='__main__':
    test = CreateSfiInstorageRequest()
    sft_lists = ['SFT-A1-20220507-5014A','SFT-A1-20220307-5006A']
    test.queryProductShiftItemToWsp(sft_lists)