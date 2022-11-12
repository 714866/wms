import jsonimport requestsfrom modular.GetApplication import get_valuefrom modular.PSR.MultipartFormData import MultipartFormDatafrom modular.Process.OAProcess import processSqlfrom modular.enums.shiptype import ShipTypefrom modular.common.SqlChangeFormat import DateEncoderfrom modular.goods.OAGoods import goodsSqlfrom modular.login import OALoginglobal oa_urloa_url = get_value('warehouse_url','url')# oa_url='http://apiewms-dev.banggood.cn/'# oa_url='http://172.16.6.203:8092/'# oa_url='http://172.16.6.32:8092/'class createPSR():    def __init__(self,oa_url):        self.oa_url=oa_url        token = OALogin.oaLoginGetToken()        self.headers = {            "Host": oa_url.split('/')[2],            "Proxy-Connection": "keep-alive",            "Content-Length": "764",            "Accept": "application/json, text/plain, */*",            # "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36",            "Origin": oa_url,            "Referer": oa_url,            # "Origin": 'http://ewms-dev.banggood.cn:8088',            # "Referer": 'http://ewms-dev.banggood.cn:8088',            "Accept-Encoding": "gzip, deflate",            "Accept-Language": "zh-CN,zh;q=0.9",            "Content-Type": "multipart/form-data; boundary=----WebKitFormBoundarywNtULNA8KNlc46BV",            "Cookie": 'Authorization="'+token+'"'        }        self.psr_path_url = oa_url+ '/warehouse/product/shift/request/createProductShiftRequestEwmsOnly?userId=33970&hostUrl='+oa_url.split('/')[2]    def postPsr(self,post_data):        """        只是组装参数与调用接口，接口返回的数据没有具体单号，        :param post_data:        :return:没有具体数据返回的        """        count = int(post_data['count_num'])        product_num = post_data['product_num']        find_process = processSql()        source_process_id = post_data['source_process_id']        source_process_name = find_process.findOaProcessNameByID(source_process_id)        source_storage= find_process.findOaStorageByProcessID(source_process_id)        source_storage_id= source_storage['storage_id']        source_storage_name= source_storage['storage_name']        targer_process_id = post_data['targer_process_id']        targer_process_name = find_process.findOaProcessNameByID(targer_process_id)        targer_storage= find_process.findOaStorageByProcessID(targer_process_id)        # targer_storage_id= targer_storage['storage_id']        # targer_storage_name= targer_storage['storage_name']        sku_code = post_data['sku_code']        sku_id = post_data['sku_id']        poa_code = post_data['poa_code']        poa_id = post_data['poa_id']        shift_type = post_data['goods_type']        ship_type = ShipType[post_data['ship_type']].value        self.data = {            "productShiftRequestCreateVOS": [                {"shiftType": shift_type,                 "priorityLevel": "0", "shipType": ship_type,                 "processCenterId": targer_process_id,                 "sourceProcessCenterId": source_process_id,                 "remark": "自写接口调用",                 "sourceProcessCenterName": source_process_name,                 "processCenterName": targer_process_name,                 "salePlatform": "", "currentPostMoney": "", "linkUrl": "", "orderNum": "",                 "salePrice": "", "grossMoney": "", "currentPostMoneyCurrency": "",                 "salePriceCurrency": "",                 "quantity": product_num,                 "productId": sku_id,                 "propertyId": poa_id,                 "storageQuantity": 3482,                 "originStorageId": source_storage_id,                 "originStorageName": targer_process_name,                 "productCode": sku_code,                 "productName": "xxx","amazonShop": "chengxidianzi01",                 "propertyCode": poa_code,                 "transferPrice": 18,                 "deliveryProductCode": "X000UOZH1B2"},]        }        mh = MultipartFormData.format(data=self.data, headers=self.headers)        i = 0        retry = False        # 调用前需要修改wsp处理中心的卡控逻辑        while i < count:            i += 1            res = requests.request("POST", data=mh.encode('utf-8'), headers=self.headers,verify=False,                                   url=self.psr_path_url)            error = res.json()['errorInfos']            if res.json()['errorInfos'] is None:                continue            error = error[0]['msg']            oa_db =goodsSql()            if error == '登陆超时，请刷新网页重新登陆':                token = OALogin.oaLoginGetToken()                self.headers['Cookie'] = 'Authorization="'+token+'"'                retry = True            elif error.find('没有AMZ经理')!=-1:                oa_db.updateGoodsAMZ(sku_id)  #补充AMZ经理                retry = True            elif error.find('处理中心转运配置')!=-1:                oa_db.inserProcessCenterTransShipPrice(source_process_id,targer_process_id,post_data['ship_type'])                retry = True            elif error.find('不支持对IT研发中心事业部服务')!=-1:                find_process.insertWspProcessDepartment(targer_process_id)                retry = True            elif error.find('不支持接收新品，请确认') != -1:                find_process.updateProcessShiftConfige(targer_process_id,'is_new_goods')                retry = True            elif error.find('调WSP处理中心尺寸重量卡控接口报错')!=-1:                find_process.updateWspProcessExpand(source_process_id)                # find_process.updateWspProcessExpand(targer_process_id)                retry = True            elif error.find('调用供应链白名单验证接口失败')!=-1:                goodsSql.updateCheckProductShiftRequest(shift_type)                retry = True            else:                raise  AssertionError("创建调拨请求报错，报错原因：{0}".format( error))            if retry:                res = requests.request("POST", data=mh.encode('utf-8'), headers=self.headers,verify=False,                                       url=self.psr_path_url)                if res.json()['errorInfos'] is not None:                    raise AssertionError("创建调拨请求报错，报错原因：{0}".format(res.json()['errorInfos'][0]['msg']))        return resclass  CreateThirdPsr(object):    def thirdPsrApiMessages(self,post_data):        thrid_psr = {}        thrid_psr['customerLabel'] = post_data['customerLabel']   #自定义SKu        thrid_psr['goodsType'] = post_data['goodsType']        thrid_psr['priorityLevel'] = 0   #调拨优先级别: 0为普通，1为紧急        thrid_psr['shipType'] = post_data['shipType']        thrid_psr['processCenterId'] = post_data['processCenterId']    #目标处理中心        thrid_psr['sourceProcessCenterId'] = post_data['sourceProcessCenterId']     #来源处理中心        thrid_psr['productId'] = post_data['productId']        thrid_psr['propertyId'] = post_data['propertyId']        thrid_psr['quantity'] = post_data['quantity']        thrid_psr['isManual'] = False   #是否手工        thrid_psr['userId'] = 50561        thrid_psr['remark'] = '测试接口生成的'        thrid_psr['isSelfPacked'] = False        thrid_psr['relatedSheetCode'] = ''  #"关联单号"        thrid_psr['shopName'] = post_data['shopName']  #"店铺"        thrid_psr['deliveryProductCode'] = post_data['deliveryProductCode']  #发货产品条码        thrid_psr['shipmentId'] = ''  #货单号        # thrid_psr['boxQuantity'] = ''  #备用参数2        # thrid_psr['fbaBoxSettingsId'] = ''  #备用参数1        #基本没用参数        thrid_psr['isWorkFlow'] = False  #是否需要推送工作流        # thrid_psr['platform'] = False  #销售平台, isWorkFlow为1时且为新品必须传入        # thrid_psr['deliverPrice'] = 1  #当地发货邮费, isWorkFlow为1时且为新品必须传入        thrid_psr['deliverCurrency'] = 'USD'  #发货币种, isWorkFlow为1时且为新品必须传入        # thrid_psr['referenceLink'] = ''  #参考链接, isWorkFlow为1时且为新品必须传入        # thrid_psr['monthOrderQuantity'] = ''  #月出单量, isWorkFlow为1时且为新品必须传入        # thrid_psr['salePrice'] = ''  #月出单量, isWorkFlow为1时且为新品必须传入        # thrid_psr['saleCurrency'] = ''  #售价币种, isWorkFlow为1时且为新品必须传入        # thrid_psr['grossProfitRatio'] = ''  #毛利率, isWorkFlow为1时且为新品必须传入        # thrid_psr['storageCode'] = ''  #仓库代码, 针对目标为美东FBW处理中心和美西FBW处理中心用于验证仓库代码是否存在且正确        #重要参数        thrid_psr['skipKx'] = True  #是否跳过库销比卡控        thrid_psr['skipCas'] = True  #是否cas验证        thrid_psr['isSplit'] = True   #是否拆单字段，拆单则不需要校验资金卡控        return thrid_psr    def requestPsrThirdApi(self,request_data,retry=False):        data_json = json.dumps(request_data,cls=DateEncoder)        print(data_json)        header={"Content-Type":"application/json"}        third_url = oa_url + '/warehouse/transfer/createThirdShipRequest?token=AT-9636-k5gws2PwFYT8fmBtLoHzA0xD0wV8ulMd'        result = requests.request('POST',data=data_json,url=third_url,headers=header)        assert result.status_code==200,'调用接口报{2}，地址{0}，参数{1}'.format(third_url,data_json,result.status_code)        error = result.json()['errorInfos']        if error is None and result.json()['success'] :            return result.json()['result']        oa_db = goodsSql()        if error[0]['msg'].find('处理中心转运配置') != -1 & retry==False:            oa_db.inserProcessCenterTransShipPrice(request_data['sourceProcessCenterId'],request_data['processCenterId'], ShipType(request_data['shipType']).name)            self.requestPsrThirdApi(request_data,retry=True)        assert error is  None,'地址{0}，参数{1}\\n 接口返回报错信息:{2}'.format(third_url,data_json,error[0]['msg'])if __name__=="__main__":    isThird=True