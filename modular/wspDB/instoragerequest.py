from datetime import datetime

from pytz import unicode

from modular.common.SqlChangeFormat import  selectChangeInser, list_to_str
from modular.wspDB.commonDB import WspCommonDB
from modular.wspDB.wspsql.instoragerequestsql import sql_get_instorage_request_by_customer, \
    sql_update_isr_request_sr_status, sql_select_isr_request


class InstorageMessage(WspCommonDB):
    def checkInstorageRequest(self,customer_order_no_list):
        """
        查询是否生成了入库升申请单
        :param customer_order_no_list:
        :return:
        """
        instorage_requests = self.cursor.fetchall(sql_get_instorage_request_by_customer.format(customer_order_no=list_to_str(customer_order_no_list)))
        return instorage_requests

    def updateInstorageRequestSrstatus(self,customer_order_no_list):
        """
        更新入库申请单sr_status状态为1，使其符合下发wms业务线条件
        :param customer_order_no_list:
        :return:
        """
        sql = sql_update_isr_request_sr_status.format(customer_order_no=list_to_str(customer_order_no_list))
        self.cursor.executeAndcommit(sql)

    def returnInsertSql(self,customer):
        sql = sql_select_isr_request.format(customer_order_no=list_to_str(customer))
        re = self.cursor.fetchall(sql)
        print(selectChangeInser(re))
        for row_dict in re:

                row_key = ','.join(str(v) for v in row_dict.keys())

                row_value = ','.join('\'' +str(v) +'\'' if isinstance(v,str) or isinstance(v, unicode) or isinstance(v,datetime) else str(v) for v in row_dict.values())

                row_value = row_value.replace('None', 'NULL')

                insert_sql = "insert into `%s`(%s) values (%s);" % ('in_storage_request', row_key, row_value)
                print(insert_sql)


if __name__=='__main__':
    t =InstorageMessage()
    t.returnInsertSql(['SFT-A1-20220307-5006A','SFT-B1-21830-00300093'])

