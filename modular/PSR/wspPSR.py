import requests


class wspPSR(object):
    def __init__(self):
        pass
    def get_oa_psr(self):
        OA_URL='172.WAREHOUSR'
        data=''
        res=requests.request('GET', url=OA_URL, data=data)
        return res
    def put_wsp(self,request_data):
        WSP_URL = ''
        data = ''
        res = requests.request('GET', url=WSP_URL, data=data)

        pass

    def find_wsp_psr_info(self):

        pass

