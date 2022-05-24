from modular.oaDB.DBConnect import OAMessage

from modular.oaDB.oasql.sftsql import sql_get_sft_to_instorage

class SftMessage(OAMessage):
    # def __init__(self):
    #     OAMessage.__init__(self)
    def getSFTtoInstorgeRequest(self,sft_list):
        """
        模拟https://ewms-oa-api.banggood.cn/oa-sync-server/syncapi/productshift/queryProductShiftItemToWsp
        接口查询主表信息sql
        :return: 主表信息 dict
        """
        self.cursor
        # print(sql_get_sft_to_instorage)
        sft_info = self.cursor.fetchall(sql_get_sft_to_instorage.format(sft_codes=sft_list))
        return sft_info





if __name__=="__main__":

    t = SftMessage()
    t.getSFTtoInstorgeRequest()