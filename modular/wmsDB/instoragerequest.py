from itertools import chain

from modular.common.SqlChangeFormat import list_to_str
from modular.common.commonDB import wmsCommonDB
from modular.wspDB.instoragerequest import InstorageMessage


class InstorageMessage1WMS(wmsCommonDB):
    def inserIsrRequest(self,insert_sqls):
            self.insertLists(insert_sqls)

    def select_isr_request(self,customers):
        """
        来源单号查询入库申请单是否存在wms库
        :param customers:   来源单号
        :return:
        """
        sql = """select customer_order_no from in_storage_request where is_deleted=0 and customer_order_no in ({0});""".format(list_to_str(customers))
        re = self.cursor.fetchall(sql)
        customers = [i['customer_order_no']  for i in re]
        return set(customers)




if __name__=='__main__':
    t =InstorageMessage1WMS()
    # wmssql = t.returnInsertSql(['SFT-B1-21830-00300094','SFT-B1-21830-00300095'])
    # g = InstorageMessage1WMS()
    # g.inserIsrRequest(wmssql)
    t.select_isr_request(['SFT-B1-21830-00300094','SFT-B1-21830-00300095'])




