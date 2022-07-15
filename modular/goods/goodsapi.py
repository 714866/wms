import json

import requests

from modular.GetApplication import get_value

wsp_url =  get_value('wsp_url','url')
wsp_key = get_value('wsp_url','key')

class GoodsApi(object):
    pass
def putOaGoodsToWsp(goods_list):
    """

    :param goods_list: 产品id列表
    :return:
    """

    get_goods_url=wsp_url + '/wsp/api/sync-download/download?key=' +wsp_key
    request_data = {
        "downloadEnum": "产品同步",
        "keyList": [""]
    }
    request_data["keyList"]=goods_list
    header = {"Content-Type": "application/json"}
    result = requests.request('POST',url=get_goods_url,headers=header,data=json.dumps(request_data))
    result.status_code==200
    # print(result)
if __name__ == "__main__":
    test1 = putOaGoodsToWsp(["2300917"])
    # test1 =