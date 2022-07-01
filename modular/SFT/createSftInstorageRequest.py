from datetime import time
import requests
import simplejson as simplejson   # 解决数据库返回Decimal类型转换成json错误使用

from modular.GetApplication import get_value
from modular.SFT.enums.shiptype import ShipType
from modular.common.SqlChangeFormat import DateEncoder, list_to_str
from modular.oaDB.getSFT import SftMessage
import json

from modular.wmsDB.instoragerequest import InstorageMessage1WMS
from modular.wspDB.instoragerequest import InstorageMessage

wsp_url = get_value('wsp_url','url')
key = get_value('wsp_url','key')

class CreateSfiInstorageRequest():
    def __init__(self):
        self.query_db = SftMessage()
        self.query_wsp_db = InstorageMessage()
        self.query_wms_db = InstorageMessage1WMS()
        pass




    def queryProductShiftItemToWsp(self,shif_codes):
        """
        替代同步系统的queryProductShiftItemToWsp接口，返回
        :param shif_codes:  调拨单号列表
        :return: 返回接口参数 类型为list
        """
        # sft_lists= self.query_db.getSFTtoInstorgeRequest(SqlChangeFormat.list_to_str(shif_codes))
        shif_codes = list_to_str(shif_codes)
        sft_lists= self.query_db.getSFTtoInstorageRequest(shif_codes)
        return self.wspApiMessages(sft_lists)

    def wspApiMessages(self,sft_lists):
        """
        s输入字段数据，返回组装数据
        :param sft_lists:
        :return:
        """
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
        print(json.dumps(product_shift_lists, cls=DateEncoder))
        return product_shift_lists

    def syncFromProductShiftInfo(self,separate_box_info_list):
        """
        调用wsp接口生成入库申请单
        :param separate_box_info_list:   syncFromProductShiftInfo接口参数
        :return: 生成入库申请单的来源单  sft
        """
        error_message=''
        header = {"Content-Type": "application/json"}
        url = wsp_url + 'wsp/api/separate-box/syncFromProductShiftInfo?key='+key
        print(url)
        res = requests.request('POST', url=url, headers=header, data=json.dumps(separate_box_info_list, cls=DateEncoder))
        sft_codes_list=[]
        for info_list in separate_box_info_list:
            sft_codes_list.append(info_list['originCode'])
        sft_codes_list = set(sft_codes_list)
        instorage_request_lists = self.query_wsp_db.checkInstorageRequest(sft_codes_list)
        if instorage_request_lists.__len__()==0:
            return '生成入库申请单失败'
        order_no = []
        for instorage_request_dict in instorage_request_lists:
            order_no.append(instorage_request_dict['customer_order_no'])
        order_no =set(order_no)
        update_codes = []
        for code in  sft_codes_list:
            if code in order_no:
                update_codes.append(code)
                continue
            else:
                error_message+='{order_no} /n'.format(order_no=order_no)
        self.query_wsp_db.updateInstorageRequestSrstatus(update_codes)
        return update_codes

    def isrFromWspToWms(self,sft_codes):
        """
        从wsp数据库查询数据，inser到wms数据库
        原因：业务线下发数据不稳定，直接自己同步数据
        :param sft_codes:
        :return:
        """
        insert_wms_isr_sql = self.query_wsp_db.returnInsertSql(sft_codes)
        self.query_wms_db.inserIsrRequest(insert_wms_isr_sql)
        return sft_codes

    def createIsrRequestToWms(self,sft_codes):
        create_info = self.queryProductShiftItemToWsp(sft_codes)
        wsp_isr = self.syncFromProductShiftInfo(create_info)
        wms_code = self.isrFromWspToWms(wsp_isr)
        return wms_code

if __name__=='__main__':
    test = CreateSfiInstorageRequest()
    sft_lists = ['SFT-A1-20220507-5014A','SFT-A1-20220307-5006A']
    separate_box_info_list=test.queryProductShiftItemToWsp(sft_lists)
    test.syncFromProductShiftInfo(separate_box_info_list)