import requests
from modular.common.SqlChangeFormat import DateEncoder
from modular.oaDB.getPsr import PsrMessage
from modular.mapper import ConnectWSPdb
from modular.wspDB.wspPsrDB import WspPsrSql
import json
from modular.GetApplication import wsp_url
from modular.wspxxlJob.xxlJob import SourceXXlJob


class CreateWspPSR(object):
    def __init__(self):
        pass
    def get_oa_psr(self,data):
        psrs = PsrMessage().findPsrMessage(data)
        return psrs
    def put_wsp(self,request_data,url):
        header={"Content-Type":"application/json"}
        WSP_URL = url
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
        res = requests.request('POST', url=WSP_URL,headers=header, data = json.dumps(data_list,cls=DateEncoder))
        source_psr = WspPsrSql().find_source_psr(psr_codes)
        return source_psr

    def find_wsp_psr_info(self):
        curse = ConnectWSPdb
        pass

    def source_to_operation(self, psr_codes):
        operation_psr_codes = SourceXXlJob().SourcePsrToOperationHandler(psr_codes)
        return operation_psr_codes

    def psr_to_pck(self,psr_codes):
        pck_order = SourceXXlJob().ShiftGenerateFileTask(psr_codes)
        return
    def psr_create_pck(self, psr_codes):
        source_request_data = self.get_oa_psr(psr_codes)
        # 返回源单的psr
        source_psr_codes = self.put_wsp(source_request_data, wsp_url)
        # 生成作业单据的psr
        operation_psr_codes = self.source_to_operation(source_psr_codes)
        # psr生成pck后，返回的psr
        pck_order = self.psr_to_pck(operation_psr_codes)

        return pck_order




if __name__=='__main__':
    test_psr = CreateWspPSR()
    psr_code =['PSR-A2-20220507-00011']
    data = test_psr.get_oa_psr(psr_code)
    test_psr.put_wsp(data,url='http://172.16.6.203:9696/wsp/api/productshiftrequest/syncSourceProductShiftRequest-back')