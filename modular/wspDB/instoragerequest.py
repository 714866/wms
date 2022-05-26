from datetime import datetime

from pytz import unicode

from modular.common.SqlChangeFormat import SqlChangeFormat
from modular.wspDB.commonDB import WspCommonDB
from modular.wspDB.wspsql.instoragerequestsql import sql_get_instorage_request_by_customer, \
    sql_update_isr_request_sr_status


class InstorageMessage(WspCommonDB):
    def checkInstorageRequest(self,customer_order_no_list):
        """
        查询是否生成了入库升申请单
        :param customer_order_no_list:
        :return:
        """
        instorage_requests = self.cursor.fetchall(sql_get_instorage_request_by_customer.format(customer_order_no=SqlChangeFormat.list_to_str(customer_order_no_list)))
        return instorage_requests

    def updateInstorageRequestSrstatus(self,customer_order_no_list):
        """
        更新入库申请单sr_status状态为1，使其符合下发wms业务线条件
        :param customer_order_no_list:
        :return:
        """
        sql = sql_update_isr_request_sr_status.format(customer_order_no=SqlChangeFormat.list_to_str(customer_order_no_list))
        self.cursor.executeAndcommit(sql)

    def returnInsertSql(self,customer):
        sql = sql_get_instorage_request_by_customer.format(customer_code=customer)

        for RowDict in sql:
                RowKey = ','.join(str(v) for v in RowDict.keys())

                RowValue = ','.join('\'' +str(v) +'\'' if isinstance(v,str) or isinstance(v, unicode) or isinstance(v,datetime.datetime) else str(v) for v in RowDict.values())

                RowValue = RowValue.replace('None', 'NULL')

                InsertSQL = "insert into `%s`(%s) values (%s);" % (TableName, RowKey, RowValue)



if __name__=='__main__':
    t =InstorageMessage
    sql_inser = t.returnInsertSql('SFT-A1-20220307-5006A')
