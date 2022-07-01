from modular.oaDB.DBConnect import OAMessage

from modular.oaDB.oasql.sftsql import sql_get_sft_to_instorage


class SftMessage(OAMessage):
    # def __init__(self):
    #     OAMessage.__init__(self)
    def getSFTtoInstorageRequest(self,sft_list):
        """
        模拟https://ewms-oa-api.banggood.cn/oa-sync-server/syncapi/productshift/queryProductShiftItemToWsp
        接口查询主表信息sql
        :return: 主表信息 dict
        """
        # print(sql_get_sft_to_instorage)
        sft_info = self.cursor.fetchall(sql_get_sft_to_instorage.format(sft_codes=sft_list))
        return sft_info

    # def checkInstorageRequest(self,customer_order_no_list):
    #
    #     instorage_requests = self.cursor.fetchall(sql_get_instorage_request_by_customer.format(customer_order_no=SqlChangeFormat.list_to_str(customer_order_no_list)))
    #     return instorage_requests

    def findExistSftCode(self, code):
        sql = "  select ProductShitItemCode from ProductShiftItem where  ProductShitItemCode like '{0}%'  ORDER BY ProductShitItemCode DESC ;".format(
            code)
        sql_result = self.cursor.fetchone(sql)
        return sql_result
    def findExistBoxCode(self,code):
        sql = "select ProductShiftBoxCode from ProductShiftBox where  ProductShiftBoxCode like '{0}%T'  ORDER BY ProductShiftBoxCode DESC ;".format(code)
        sql_result = self.cursor.fetchone(sql)
        return sql_result
if __name__=="__main__":

    t = SftMessage()
    t.getSFTtoInstorageRequest()