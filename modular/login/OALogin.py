import requests

url_api = "https://castest.banggood.cn/cas/oauth2.0/accessToken?grant_type=password&client_id=123456&client_secret=123456&username=zhuzhiliang%40banggood.com&password=Bg%40753951%21"
headers = {
    "service": "https://castest.banggood.cn",
    "Content-Type": "application/json;charset=UTF-8"
}
def oaLoginGetToken():
    token = requests.get(url=url_api,headers=headers).json()
    return 'Bearer '+ token['access_token']




if __name__ == '__main__':
    oaLoginGetToken()