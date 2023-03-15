from itertools import chain

from modular.common.SqlChangeFormat import list_to_str
from modular.common.commonDB import wmsCommonDB
from modular.wspDB.instoragerequest import InstorageMessage

inserSql = """INSERT INTO `ews`.`outbound_group_config` (`id`, `delivery_type`, `batch_model`, `group_type`, `priority`, `is_limit`,
                                           `limit_quantity`, `is_open`, `is_hint`, `processcenter_id`, `create_date`,
                                           `create_user_id`, `create_user_name`, `modify_date`, `modify_user_id`,
                                           `modify_user_name`, `is_deleted`, `delete_date`, `delete_user_id`,
                                           `lock_version`, `modify_time_stamp`, `is_used`, `is_partial`)
VALUES ('{0}', '{1}', '{2}', '{3}', '2', '1', '1', '1', '1', '{4}', '1970-01-01 00:00:00', '0', '',
        '2020-10-21 16:51:49', '656071542958202880', '朱志亮', '0', '1970-01-01 00:00:00', '0', '0', '2020-10-21 16:51:48',
        '{5}', '0');
"""

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

    def inserOutbountConfig(self,delivery_type, processcenter):
        # cursor = connect_DB(wms_db)
        selectSql = 'select * from outbound_group_config ORDER BY id DESC LIMIT 1 '
        newId = int(self.cursor.fetchone(selectSql)['id'])+1
        # newId=85974589388221085
        # print(newId)
        for i in range(0, 9):
            print(i)
            if i <= 5:
                self.cursor.execute(inserSql.format(newId + i, delivery_type, 0, i + 1, processcenter, 1))
            else:
                self.cursor.execute(inserSql.format(newId + i, delivery_type, 1, i - 4, processcenter, 0))
        self.cursor.commitAndClose()


if __name__=='__main__':
    t =InstorageMessage1WMS()
    # wmssql = t.returnInsertSql(['SFT-B1-21830-00300094','SFT-B1-21830-00300095'])
    # g = InstorageMessage1WMS()
    # g.inserIsrRequest(wmssql)
    # t.select_isr_request(['SFT-B1-21830-00300094','SFT-B1-21830-00300095'])



    #设置处理中心
    processcenter = 934
    #设置销售类型
    delivery_type = 0
    t.inserOutbountConfig(delivery_type,processcenter)




