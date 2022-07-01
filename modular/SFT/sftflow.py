import requests

from modular.GetApplication import get_value

global oa_url
global oa_url_key
oa_url = get_value('warehouse_url','url')
oa_url_key = get_value('warehouse_url','key')
class SftFlow(object):
    def createOaSFT(self,request_data):
        """

        :param data:
        :return:
        """
        #模拟接口http://172.16.6.203:8092/warehouse/syncapi/shift/syncProductShiftByWms-back


        headers = {"Content-Type": "application/json"}
        sft_api_url = oa_url + "/warehouse/syncapi/shift/syncProductShiftByWms-back?key=" + oa_url_key
        response_data = requests.request("POST",  headers=headers,url=sft_api_url,data=request_data)

        print(response_data)
        pass