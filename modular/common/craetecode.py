import time

# now_date = time.strftime("%Y%m%d", time.localtime())
# sft_code_start = 'SFT-T1'
# sft_code = 'SFT-T1-'+time.strftime("%Y%m%d", time.localtime())
from modular.oaDB.getSFT import SftMessage
from modular.wspDB.instoragerequest import InstorageMessage
from wmspda.models import OdsPckInfo

class GetCode(object):
    __instance = None
    def __new__(cls, *args, **kwargs):
        # 类对象唯一
        if cls.__instance is None:
            cls.__instance = super(GetCode, cls).__new__(cls)
        return cls.__instance
    def __init__(self):
        self.wsp_db = InstorageMessage()
        self.oa_db = SftMessage()


    def getSftCode(self,count):
        """
        传入需要返回调拨单
        :param count:
        :return:['SFT-T1-20220616-00001', 'SFT-T1-20220616-00002']
        """
        sft_codes = []
        now_date = time.strftime("%Y%m%d", time.localtime())
        code = 'SFT-T1-' + time.strftime("%Y%m%d", time.localtime())
        # code = 'SFT-O1-20210407'
        exist_sft_code = self.wsp_db.findExistSftCode(code)
        if exist_sft_code==None:
            for i in range(count):
                sft_code = code + '-' + str(i+1).zfill(5)
                sft_codes.append(sft_code)
        else:
            #提取数字
            # exist_sft_code['']
            lists = exist_sft_code['customer_order_no'].split('-')
            exist_sft_code_num = exist_sft_code['customer_order_no'].split('-')[3]
            num = ''.join(list(filter(str.isdigit, exist_sft_code_num)))
            for i in range(count):
                num = str(int(num)+1).zfill(5)
                sft_code = code + '-' + num
                sft_codes.append(sft_code)

        return sft_codes

    def getboxCode(self, count):
        """
             传入需要返回分箱数
             :param count:
             :return:['SFT-T1-20220616-00001', 'SFT-T1-20220616-00002']
        """
        box_codes = []
        # now_date = time.strftime("%Y%m%d", time.localtime())
        code = 'FBOX-' + time.strftime("%Y%m%d", time.localtime())
        # code = 'SFT-O1-20210407'
        exist_box_code = self.wsp_db.findExistBoxCode(code)
        if exist_box_code == None:
            for i in range(count):
                box_code = code + '-' + str(i + 1).zfill(5) + 'T'
                box_codes.append(box_code)
        else:
            # 提取数字
            # exist_sft_code['']
            exist_sft_code_num = exist_box_code['box_code'].split('-')[2]
            num = ''.join(list(filter(str.isdigit, exist_sft_code_num)))
            for i in range(count):
                num = str(int(num) + 1).zfill(5)
                box_code = code + '-' + num + 'T'
                box_codes.append(box_code)
        return box_codes

    def getPPLCode(self,count):
        ppl_codes = []
        code = 'PPL-' + time.strftime("%Y%m%d", time.localtime())
        exist_PPL_code = self.wsp_db.findExistPplCode(code)
        if exist_PPL_code == None:
            for i in range(count):
                ppl_code = code + '-' + str(i + 1).zfill(5)
                ppl_codes.append(ppl_code)
        else:
            # 提取数字
            # exist_sft_code['']
            # lists = exist_PPL_code['source_code'].split('-')
            exist_sft_code_num = exist_PPL_code['source_code'].split('-')[2]
            num = ''.join(list(filter(str.isdigit, exist_sft_code_num)))
            for i in range(count):
                num = str(int(num) + 1).zfill(5)
                ppl_code = code + '-' + num
                ppl_codes.append(ppl_code)
        return ppl_codes

    def getOaSFTCode(self,count):
        sft_codes = []
        now_date = time.strftime("%Y%m%d", time.localtime())
        code = 'SFT-T1-' + time.strftime("%Y%m%d", time.localtime())
        # code = 'SFT-O1-20210407'
        exist_sft_code = self.oa_db.findExistSftCode(code)
        if exist_sft_code == None:
            for i in range(count):
                sft_code = code + '-' + str(i + 1).zfill(5)
                sft_codes.append(sft_code)
        else:
            # 提取数字
            # exist_sft_code['']
            # lists = exist_sft_code['ProductShitItemCode'].split('-')
            exist_sft_code_num = exist_sft_code['ProductShitItemCode'].split('-')[3]
            num = ''.join(list(filter(str.isdigit, exist_sft_code_num)))
            for i in range(count):
                num = str(int(num) + 1).zfill(5)
                sft_code = code + '-' + num
                sft_codes.append(sft_code)
        return sft_codes

    def getOaBoxCode(self,count):
        box_codes = []
        # now_date = time.strftime("%Y%m%d", time.localtime())
        code = 'FBOX-' + time.strftime("%Y%m%d", time.localtime())
        exist_box_code = self.oa_db.findExistBoxCode(code)
        if exist_box_code == None:
            for i in range(count):
                box_code = code + '-' + str(i + 1).zfill(5) + 'T'
                box_codes.append(box_code)
        else:
            # 提取数字
            # exist_sft_code['']
            exist_sft_code_num = exist_box_code['ProductShiftBoxCode'].split('-')[2]
            num = ''.join(list(filter(str.isdigit, exist_sft_code_num)))
            for i in range(count):
                num = str(int(num) + 1).zfill(5)
                box_code = code + '-' + num + 'T'
                box_codes.append(box_code)
        return box_codes
    def get_twms_pck_code(self,process,count=1):
        pck_code = []
        code ='PCK'+str(process).zfill(4)+time.strftime('%y%m%d',time.localtime())
        exist_pck_info = OdsPckInfo.objects.using('twms').filter(pck_code__iexact=code)['']
        if exist_pck_info == None:
            pass




if __name__=='__main__':
    test = GetCode()
    print(test)
    print(test.get_twms_pck_code(1038))


