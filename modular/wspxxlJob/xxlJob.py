import requests
from modular.wspDB import wspPsrDB
wsp_xxl_url='http://172.16.6.203:9696/wsp/page/product-shift-monitor-config/executeJob?jobName='
class SourceXXlJob(object):
    def __init__(self):
        pass

    def SourcePsrToOperationHandler(self,source_psr_codes,job_name="SourcePsrToOperationHandler"):
        result = requests.get(url=wsp_xxl_url+job_name)
        wsp_db = wspPsrDB.WspPsr()
        operation_psr_codes = wsp_db.find_psr(source_psr_codes)
        return  operation_psr_codes

    def ShiftGenerateFileTask(self,operation_psr_codes,job_name='ShiftGenerateFileTask'):
        """
        生成文件服务
        psr 最终升才pck，  且服务会根据模板处理中心来判断生成文件逻辑，为了保证流程正常走，
        调用前先将处理中心换成无需生成文件的处理中心  取的数据源是OA的
        :param operation_psr_codes:
        :param job_name:
        :return: 返回生成pck的调拨请求
        """
        result = requests.get(url=wsp_xxl_url+job_name)
        wsp_db =wspPsrDB.WspPsr()
        pck_order = wsp_db.find_pck_by_psr(operation_psr_codes)



if __name__=='__main__':
    lists = ['PSR-A2-20220507-00011']
    t = SourceXXlJob().ShiftGenerateFileTask(lists)


