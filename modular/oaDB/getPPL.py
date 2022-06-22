from modular.oaDB.DBConnect import OAMessage

from modular.oaDB.oasql.PPLsql  import sql_get_PPL_to_instorage


class PPLMessage(OAMessage):
    # def __init__(self):
    #     OAMessage.__init__(self)
    def getPPLtoInstorageRequest(self,ppl_list):
        """
        模拟https://ewms-oa-api.banggood.cn/oa-sync-server/syncapi/productshift/queryProductShiftItemToWsp
        接口查询主表信息sql
        :return: 主表信息 dict
        """
        # print(sql_get_sft_to_instorage)
        ppl_info = self.cursor.fetchall(sql_get_PPL_to_instorage.format(ppl_list))
        return ppl_info

    # def checkInstorageRequest(self,customer_order_no_list):
    #
    #     instorage_requests = self.cursor.fetchall(sql_get_instorage_request_by_customer.format(customer_order_no=SqlChangeFormat.list_to_str(customer_order_no_list)))
    #     return instorage_requests



if __name__=="__main__":

    t = PPLMessage()
    re = t.getPPLtoInstorageRequest('PPL-20190521-372385')
    print(re)