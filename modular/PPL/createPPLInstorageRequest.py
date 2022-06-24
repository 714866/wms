from datetime import time
import requests
import simplejson as simplejson   # 解决数据库返回Decimal类型转换成json错误使用

from modular.GetApplication import get_value
from modular.SFT.enums.shiptype import ShipType
from modular.common.SqlChangeFormat import DateEncoder, list_to_str
from modular.oaDB.getPPL import PPLMessage
import json

from modular.wmsDB.instoragerequest import InstorageMessage1WMS
from modular.wspDB.instoragerequest import InstorageMessage
from modular.wspxxlJob.xxlJob import SourceXXlJob

wsp_url = get_value('wsp_url','url')
key = get_value('wsp_url','key')

class CreatePPLInstorageRequest():
    def __init__(self):
        self.query_db = PPLMessage()
        self.query_wsp_db = InstorageMessage()
        self.query_wms_db = InstorageMessage1WMS()
        pass



    def queryPPLToWsp(self,ppl_codes):
        """http://172.16.6.203:9996/oa-sync-server/syncapi/purchase-package/queryPurchasePackageInfo?packageId=186607721&processCenterIds=1150&top=500
        替代同步系统的接口，返回
        :param shif_codes:  调拨单号列表
        :return: 返回接口参数 类型为list
        """
        # ppl_lists= self.query_db.getppltoInstorgeRequest(SqlChangeFormat.list_to_str(shif_codes))
        ppl_codes = list_to_str(ppl_codes)
        ppl_lists= self.query_db.getPPLtoInstorageRequest(ppl_codes)
        return self.wspApiMessages(ppl_lists)

    def wspApiMessages(self,ppl_lists):
        """
        s输入字段数据，返回组装数据
        :param ppl_lists 数据库查询回来的结果
        :return:
        """
        ppl_instorage_lists = []   #  # 存储 [{api_info},{api_info}]
        # ppl_instorage_dicts = {}   #存放总调用字典数据  {ppl_code:{api_info}}
        # ppl_instorage_dict = {}  # 存放子调用字典数据{api_info}
        for ppl_list in ppl_lists:
            is_not_exit = True
            ppl_instorage={}
            for p in  ppl_instorage_lists:
                ppl_instorage = {}
                ppl_instorage['originProcessCenterId']=  ppl_list['OriginProcessCenterId']
                ppl_instorage['targetProcessCenterId']=  ppl_list['TargetProcessCenterId']
                ppl_instorage['shipType'] =  ppl_list['ShipType']
                ppl_instorage['lastUpdateTime'] =  ppl_list['LastUpdateTime']
                ppl_instorage['lastUpdateUserId'] =  ppl_list['LastUpdateUserID']
                ppl_instorage['quantity'] =  ppl_list['Quantity']
                ppl_instorage['productId'] =  ppl_list['ProductID']
                ppl_instorage['propertyId'] =  ppl_list['PropertyID']
                ppl_instorage['isTest'] =  ppl_list['IsTest']
                ppl_instorage['goodsType'] =  ppl_list['GoodsType']
                ppl_instorage['vacuumPacking'] =  ppl_list['vacuumPacking']
                ppl_instorage['isShiftCosting'] =  ppl_list['IsShiftCosting']
                ppl_instorage['goodsSize'] =  ppl_list['goodsSize']
                ppl_instorage['salePlatform'] =  ppl_list['salePlatform']
                ppl_instorage['packageId'] =  ppl_list['PackageID']
                ppl_instorage['packageCode'] =  ppl_list['packageCode']
                #lclLimitLevel 在原代码中是判断货物类型为21的则不允许拼箱，不为21允许相同货主拼箱
                ppl_instorage['lclLimitLevel'] = "允许相同货主拼箱"
                ppl_instorage['storageCode'] =  ppl_list['storageCode']
                ppl_instorage['amazonShop'] =  ppl_list['AmazonShop']
                ppl_instorage['deliveryProductCode'] =  ppl_list['deliveryProductCode']
                ppl_instorage['isDrowback'] =  ppl_list['isDrowback']
                ppl_instorage['shipmentId'] =  ppl_list['shipmentId']
                ppl_instorage['createUserId'] =  ppl_list['CreateUserID']
                ppl_instorage['createTime'] =  ppl_list['CreateTime']
                ppl_instorage_lists.append(ppl_instorage)  # 加到主表中
                # print(ppl_instorage)
        print(json.dumps(ppl_instorage_lists, cls=DateEncoder))
        return ppl_instorage_lists

    def syncFromPPL(self,ppl_info):
        """
        调用wsp接口生成入库申请单
        :param separate_box_info_list:   syncFromPPL
        :return: 生成入库申请单的来源单  ppl
        """
        error_message=''
        header = {"Content-Type": "application/json"}
        url = wsp_url + '/wsp/api/in-storage-request/syncFromPPL-back?key='+key
        print(json.dumps(ppl_info, cls=DateEncoder))
        #在wsp生成PPL源单
        res = requests.request('POST', url=url, headers=header, data=json.dumps(ppl_info, cls=DateEncoder))
        #对PPL源单生成作业单
        SourceXXlJob.xxlJobAction('SourceToInStorageRequestTask')
        ppl_codes_list=[]
        for info_list in ppl_info:
            ppl_codes_list.append(info_list['packageCode'])
        ppl_codes_list = set(ppl_codes_list)
        instorage_request_lists = self.query_wsp_db.checkInstorageRequest(ppl_codes_list)
        if instorage_request_lists.__len__()==0:
            return '生成入库申请单失败'
        order_no = []
        for instorage_request_dict in instorage_request_lists:
            order_no.append(instorage_request_dict['customer_order_no'])
        order_no =set(order_no)
        update_codes = []
        for code in  ppl_codes_list:
            if code in order_no:
                update_codes.append(code)
                continue
            else:
                error_message+='{order_no} /n'.format(order_no=order_no)
        self.query_wsp_db.updateInstorageRequestSrstatus(update_codes)
        return update_codes

    def isrFromWspToWms(self,ppl_codes):
        """
        从wsp数据库查询数据，inser到wms数据库
        原因：业务线下发数据不稳定，直接自己同步数据
        :param ppl_codes:
        :return:
        """
        insert_wms_isr_sql = self.query_wsp_db.returnInsertSql(ppl_codes)
        self.query_wms_db.inserIsrRequest(insert_wms_isr_sql)
        return ppl_codes

    def createIsrRequestToWms(self,ppl_codes):
        create_info = self.queryPPLToWsp(ppl_codes)
        wsp_isr = self.syncFromPPL(create_info)
        wms_code = self.isrFromWspToWms(wsp_isr)
        return wms_code

if __name__=='__main__':
    test = CreatePPLInstorageRequest()
    ppl_lists = ['PPL-20190520-363856','PPL-20190521-372385']
    separate_box_info_list=test.queryPPLToWsp(ppl_lists)
    test.syncFromPPL(separate_box_info_list)