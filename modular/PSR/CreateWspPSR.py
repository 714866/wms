import requests
from modular.common.SqlChangeFormat import DateEncoder, list_to_str
from modular.oaDB.getPsr import PsrMessage, find_psr
from modular.mapper import ConnectWSPdb
from modular.wspDB.wspPsrDB import WspPsrSql
import json
# from modular.GetApplication import wsp_url
from modular.wspxxlJob.xxlJob import SourceXXlJob

from modular.GetApplication import get_value

wsp_url = get_value('wsp_url','url')
wsp_key = get_value('wsp_url','key')
class CreateWspPSR(object):
    def __init__(self):
        pass
    def get_oa_psr(self,data):
        psrs = PsrMessage().findPsrMessage(data)
        print ('查询PSR下发信息{0}'.format(psrs))
        assert  len(psrs) != 0,('在OA查询无数据,{0}'.format(find_psr.format(list_to_str(data))))
        return psrs
    def put_wsp(self,request_data):
        header={"Content-Type":"application/json"}
        url = wsp_url + '/wsp/api/productshiftrequest/syncSourceProductShiftRequest-back'
        data_list=[]
        psr_codes = []
        for r in request_data:

            data_dict = {'productShiftRequestCode':r['productShiftRequestCode'],
                         'productId':r['productId'],
                         'propertyId':r['propertyId'],
                         'quantity':r['quantity'],
                         'originProcessCenterId':r['originProcessCenterId'],
                         'targetProcessCenterId':r['targetProcessCenterId'],
                         'shipType':r['shipType'],
                         'baseProductCode':r['baseProductCode'],
                         'priorityLevel':r['priorityLevel'],
                         'storageCode':r['storageCode'],
                         'goodsType':r['goodsType'],
                         'deliveryProductCode':r['deliveryProductCode'],
                         'isSelfPacked':r['isSelfPacked'],
                         'isFullBox':r['isFullBox'],
                         'shipmentId':r['shipmentId'],
                         'boxQuantity':r['boxQuantity'],
                         'modifyTimeStamp':r['modifyTimeStamp'],
                         'amazonShop':r['amazonShop'],
                         'amazonCustomerLabel':r['amazonCustomerLabel'],
                         'createDate':r['CreateDate'],
                         'auditTime':r['AuditTime'],
                         'lastUpdateTime':r['LastUpdateTime'],
                         'goodsSize':r['goodsSize']
                        }
            data_list.append(data_dict)
            psr_codes.append(r['productShiftRequestCode'])
        res = requests.request('POST', url=url, headers=header, data = json.dumps(data_list,cls=DateEncoder))
        operate_url =  wsp_url + '/wsp/api/product-shift-request/createProductShiftRequest-back?key='+wsp_key
        operate = requests.request('POST', url=operate_url, headers=header, data = json.dumps(data_list,cls=DateEncoder),verify=False)
        source_psr = WspPsrSql().find_source_psr(psr_codes)
        print('生成调拨请求源单{0}'.format(source_psr))
        return source_psr

    def find_wsp_psr_info(self):
        curse = ConnectWSPdb
        pass

    def source_to_operation(self, psr_codes):
        """
        PSR源单生成PSR作业单
        :param psr_codes:
        :return:
        """
        operation_psr_codes = SourceXXlJob().SourcePsrToOperationHandler(psr_codes)
        return operation_psr_codes

    def psr_to_pck(self,psr_codes):
        """
        s调用接口生成pck
        :param psr_codes:
        :return:
        """
        pck_order = SourceXXlJob().apiGenerateFile(psr_codes)
        return pck_order

    def psr_create_pck(self, psr_codes):
        source_request_data = self.get_oa_psr(psr_codes)
        # 返回源单的psr
        source_psr_codes = self.put_wsp(source_request_data)
        # 生成作业单据的psr
        # source_request_data['productId']
        # source_request_data['propertyId']
        operation_psr_codes = self.source_to_operation(psr_codes)
        # psr生成pck后，返回的psr
        pck_order = self.psr_to_pck(operation_psr_codes)

        return pck_order




if __name__=='__main__':
    test_psr = CreateWspPSR()
    psr_code =['PSR-A2-20220627-00002']
    data = test_psr.get_oa_psr(psr_code)
    source_psr_codes = test_psr.put_wsp(data)
    operation_psr_codes = test_psr.source_to_operation(source_psr_codes)
    # test_psr.put_wsp(data,url='http://172.16.6.203:9696/wsp/api/productshiftrequest/syncSourceProductShiftRequest-back')