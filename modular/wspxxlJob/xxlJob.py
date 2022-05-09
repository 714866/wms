import json

import requests

from modular.oaDB.getPsr import PsrMessage
from modular.wspDB.wspPsrDB import WspPsrSql
from modular.GetApplication import get_value


wsp_xxl_url = get_value('wsp_url') + '/wsp/page/product-shift-monitor-config/executeJob?jobName='
class SourceXXlJob(object):
    def __init__(self):
        self.wsp_db = WspPsrSql()
        pass

    def SourcePsrToOperationHandler(self, source_psr_codes, job_name="SourcePsrToOperationHandler"):
        result = requests.get(url=wsp_xxl_url+job_name)
        operation_psr_codes = self.wsp_db.find_operation_psr(source_psr_codes)
        return  operation_psr_codes

    def ShiftGenerateFileTask(self, operation_psr_codes, job_name='ShiftGenerateFileTask'):
        """
        生成文件服务
        psr 最终升才pck，  且服务会根据模板处理中心来判断生成文件逻辑，为了保证流程正常走，
        调用前先将处理中心换成无需生成文件的处理中心  取的数据源是OA的
        :param operation_psr_codes:
        :param job_name:
        :return: 返回生成pck的调拨请求
        """
        result = requests.get(url=wsp_xxl_url+job_name)
        pck_order = self.wsp_db.find_pck_by_psr(operation_psr_codes)
        return pck_order

    def apiGenerateFile(self, operation_psr_codes):
        """
        使用接口调用生成文件逻辑，能按传参，生成pck
        :param operation_psr_codes:  需执行调拨请求列表
        :return:
        """
        psr = PsrMessage()
        # 正常来说一批单都是同处理中心的
        targe_process_id = psr.findTargeProcess(operation_psr_codes[0])
        psr.updatePsrTargeProcess(operation_psr_codes,1111)
        header={"Content-Type": "application/json"}
        api_url = get_value('wsp_url') + "wsp/api/product-shift-request/generateFile?key=UDDD6TZ7ZP6ZCGD5IUQQUP1AGL50T5MK9U0KQQ16XEK2SS6Y1A43TABL2ZAPGT1C&delete=false"
        try:
            result = requests.request('POST',url=api_url, headers=header, data=json.dumps(operation_psr_codes))
        except:
            pass
        finally:
            psr.updatePsrTargeProcess(operation_psr_codes, targe_process_id)
        pck_order = self.wsp_db.find_pck_by_psr(operation_psr_codes)
        return pck_order
        # res = requests.request('POST', url=WSP_URL,headers=header, data = json.dumps(data_list,cls=DateEncoder))



if __name__=='__main__':
    lists = ['PSR-A2-20220507-00011']
    t = SourceXXlJob().apiGenerateFile(lists)


