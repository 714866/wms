
import requests

class wmsRequest(object):
    session_request = requests.Session()

    def __init__(self,if_login=True):
        self.session = requests.session()
        self.header = {"Content-Type": "application/json;charset=UTF-8"}
        login_url = 'http://172.16.7.4:18201/own-wms-api/pda/sys-user/login'
        d = {
            "language": 0,
            "password": "123456",
            "username": "zhuzhiliang@banggood.com"
        }
        if if_login :
            self.session.post(url=login_url,json=d,headers=self.header)

    def login(self,param):
        login_url = 'http://172.16.7.4:18201/own-wms-api/pda/sys-user/login'
        d = {
            "language": 0,
            "password": param['password'],
            "username": param['username']
        }
        self.session.post(url=login_url, json=d, headers=self.header)
