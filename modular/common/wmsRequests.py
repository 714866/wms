import json
import requests
from django.db import connection

from modular.common.GlobalApiUrl import wms_url

#wms后端地址
wms_api_url = wms_url()

class wmsRequest(object):
    session_request = requests.Session()
    def __init__(self,is_login=True):
        """

        :param is_login: 是否需要登录
        """

        self.session = requests.session()
        self.header = {"Content-Type": "application/json;charset=UTF-8"}
        # self.wms_api_url=wms_url()
        # login_url = 'http://172.16.11.39:18201/own-wms-api/pda/sys-user/login'
        if is_login :
            login_url = wms_api_url + '/own-wms-api/pda/sys-user/login'
            d = {
                "language": 0,
                "password": "123456",
                "username": "zhuzhiliang@banggood.com"
            }
            self.session.post(url=login_url,json=d,headers=self.header)

    def login(self,param):
        login_url = wms_api_url+'/own-wms-api/pda/sys-user/login'
        post_data = {
            "language": 0,
            "password": param['password'],
            "username": param['username']
        }
        self.session.post(url=login_url, json=post_data, headers=self.header)

    def update_user_processcenter(self,processcenter):
        """
        切换手持登录处理中心
        :param processcenter:
        :return:
        """
        url = wms_api_url+"/own-wms-api/pda/sys-user/updateUserProcessCenter?processCenterId="+str(processcenter)
        self.session.get(wms_api_url)



    def save_shelf(self,param):
        """
        入库签收
        :param param:
        :return:
        """
        save_shelf_url = wms_api_url+"/own-wms-api/pda/shelf/saveShelf"
        order_code = {"targetCode":param}
        result = self.session.post(url=save_shelf_url,json=order_code)
        result_text = json.loads(result.text)
        print(result_text)
        if result_text['errorInfos'] is not None:
            # 判断是否有报错信息
            return {"error":True,"error_info":result_text['errorInfos'][0]}
        return {"error":False,"message":result_text}

    def save_receipt(self,param):
        """
        收货
        :param param:
        :return:
        """
        items = []
        post_data = {
            "inStorageRequestNo": param[0].get('in_storage_request_no'),
            "items": items,
            "receiptTypeEnum": 0
        }
        for item_list in param:
            item = {}
            item['itemId'] = item_list.get('id')
            item['quantity'] = item_list.get('plan_receipt_quantity')
            items.append(item)
        api_url = wms_api_url + "/own-wms-api/pda/receipt/saveReceipt"
        api_result = self.session.post(url=api_url,json=post_data)
        api_result = json.loads(api_result.text)
        return api_result

    def save_instorage(self,param):
        """
        入库
        :param param:
        :return:
        """
        api_url = wms_api_url+'/own-wms-api/pda/inStorage/saveInStorage'
        post_data = {'receiptNo':param}
        api_result = self.session.post(url=api_url,json=post_data)
        if len(json.loads(api_result.text)['errorInfos']) > 0:
            print(api_result.text)
            return json.loads(api_result.text)['errorInfos']
        return json.loads(api_result.text)

    def update_shelf_rack(self,params):
        """
        s上架
        :param param:[{
        "goodsId":"1073909340791595008",
        "quantity":1,
        "rack":"A-A-01",
        "scanCode":"Fbox-20230211-00002",
        "shelfCode":"SJ2023021100003A",
        "uniqueCode":""
    }]
        :return:
        """
        api_url = wms_api_url + '/own-wms-api/pda/shelf/updateShelfRack'
        post_data=[]
        for param in params:
            shelf_dict = {
                "goodsId": param.get('goods_id'),
                "quantity": param.get('quantity'),
                "rack": param.get('rack'),
                "scanCode": param.get('source_code'),
                "shelfCode": param.get('shelf_code'),
                "uniqueCode": ""
            }
            post_data.append(shelf_dict)
        result = self.session.post(url=api_url,json=post_data)
        return json.loads(result.text)

    def pda_allocation_task_save(self,tx_code):
        get_task_api_url = wms_api_url+'/own-wms-api/pda/allocation-task/getBatchAllocationData?batchBarCode='+tx_code
        get_task_result = self.session.get(url=get_task_api_url)
        task_result = json.loads(get_task_result.text)['result']

        save_param = {
            "commandId": task_result[0]['commandId'],
            "quantity": task_result[0]['quantity'],
            "containerCode": "",
            "taskCode": "",
            "rackCode": task_result[0]['rack'],
            "batchModelEnum": "纸质配货"
        }
        save_api_url = wms_api_url+'/own-wms-api/pda/allocation-task/save'
        save_result = self.session.post(url=save_api_url,json=save_param)
        return json.loads(save_result.text)


