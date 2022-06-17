from datetime import datetime

from pytz import unicode

from modular.common.SqlChangeFormat import  selectChangeInsert, list_to_str
from modular.common.commonDB import WspCommonDB

from modular.wspDB.wspsql.instoragerequestsql import sql_get_instorage_request_by_customer, \
    sql_update_isr_request_sr_status, sql_select_isr_request, sql_select_isr_box, sql_select_isr_box_item


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
        #获取入库申请主表，并组装插入sql
        sql = sql_select_isr_request.format(customer_order_no=list_to_str(customer))
        isr_main = self.cursor.fetchall(sql)
        isr_main_insert_sql = selectChangeInsert('in_storage_request',isr_main)
        print(isr_main_insert_sql)
        #获取入库申请分箱表，并组装插入sql
        in_storage_request_ids =  ','.join('\''+str(isr['id'])+'\'' for isr in isr_main)
        isr_box = self.cursor.fetchall(sql_select_isr_box.format(in_storage_request_id = in_storage_request_ids))
        isr_box_insert_sql = selectChangeInsert('in_storage_request_box',isr_box)
        print(isr_box_insert_sql)

        #获取入库申请分箱明细表，并组装插入sql
        isr_box_ids =  ','.join('\''+str(isr['id'])+'\'' for isr in isr_box)
        isr_box_item = self.cursor.fetchall(sql_select_isr_box_item.format(isr_box_id=isr_box_ids))
        isr_item_insert_sql = selectChangeInsert('in_storage_request_box_item',isr_box_item)
        print(isr_item_insert_sql)

        return [isr_main_insert_sql,isr_box_insert_sql,isr_item_insert_sql]

    def findGoodsInfo(self,goods_code):
        """

        :param goods_code:
        :return:
        """
        # start_code = goods_code[0:3].upper()
        # if start_code == "PBU":
        pbu_sql='select * from goods where is_deleted=0 and  base_product_code={0});'.format(goods_code)
        select_result = self.cursor.fetchone(pbu_sql)
        return select_result
        # elif start_code == "SKU":
        #     sku_sql='select g.* from goods g inner join goods_bar_code gbc on gbc.goods_id=g.id where gbc.goods_code={0};'.format(goods_code)
        #     select_result = self.cursor.fetchone(sku_sql)
        # else:
        #
        #     pass
    def findExistSftCode(self,code):
        sql = "select box_code from in_storage_request_box where  box_code like '{0}%T'  ORDER BY box_code DESC ;".format(code)
        sql_result = self.cursor.fetchone(sql)
        return sql_result

    def findExistBoxCode(self,code):
        sql = "select box_code from in_storage_request_box where  box_code like '{0}%T'  ORDER BY box_code DESC ;".format(code)
        sql_result = self.cursor.fetchone(sql)
        return sql_result

if __name__=='__main__':
    t =InstorageMessage()
    t.returnInsertSql(['SFT-A1-20220307-5006A','SFT-B1-21830-00300093'])

