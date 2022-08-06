from modular import mapper
from modular.common.SqlChangeFormat import list_to_str, selectChangeInsert
from modular.wspDB.wspsql.PsrSql import sql_select_pck_info, sql_select_pck_item, sql_select_psr, sql_select_psr_item


class WspPsrSql(object):
    find_source_psr_sql = """
select product_shift_request_code
from source_product_shift_request where is_deleted=0 and  product_shift_request_code in ({0});
    """
    find_operation_psr_sql = """
    select product_shift_request_code
    from product_shift_request
    where is_deleted = 0
      and product_shift_request_code in ({0});"""

    find_pck_by_psr_sql="""select id,package_id,order_id
from package_info where order_id in ({0});
    """
    # __instance = None
    # def __new__(cls, *args, **kwargs):
    #     # 类对象唯一
    #     if cls.__instance is None:
    #         cls.__instance = super(WspPsrSql, cls).__new__(cls)
    #     return cls.__instance
    def __init__(self):
        self.cursor = mapper.ConnectWSPdb()

    def find_source_psr(self,psr_codes):
        sql = self.find_source_psr_sql.format(list_to_str(psr_codes))
        sql_result = self.cursor.fetchall(sql)
        source_psr_codes = []
        for psr_code in psr_codes:
            for psr_message in sql_result:
                is_true = 0
                if psr_code in psr_message.values():
                    is_true = 1
                    source_psr_codes.append(psr_code)
                    break
            if is_true==0:
                print('{0}未生成psr来源单据'.format(psr_code))
        assert  len(source_psr_codes) != 0,('全部数据未生成psr来源单据,{0}'.format(psr_codes))
        return source_psr_codes
    def find_operation_psr(self,psr_codes):
        '''
        查询psr源单是否生成作业单
        :param psr_codes:
        :return:operation_psr_codes    已生成作业单的调拨单
        '''
        sql = self.find_operation_psr_sql.format(list_to_str(psr_codes))
        psr_messages = self.cursor.fetchall(sql)
        operation_psr_codes=[]
        for psr_code in psr_codes:
            for psr_message in psr_messages:
                is_true = 0
                if psr_code in psr_message.values():
                    is_true=1
                    operation_psr_codes.append(psr_code)
                    break
            if is_true == 0:
                print('{0}未生成psr作业单据'.format(psr_code))
        assert  len(operation_psr_codes) != 0,('全部数据未生成psr作业单据,{0}'.format(psr_codes))
        return operation_psr_codes

    def find_pck_by_psr(self,psr_codes):
        psr_codes_str = list_to_str(psr_codes)
        sql = self.find_pck_by_psr_sql.format(psr_codes_str)
        pck_messages = self.cursor.fetchall(sql)
        pck_orders_codes = []
        is_true = 0
        for psr_code in psr_codes:
            for psr_message in pck_messages:
                if psr_code in psr_message.values():
                    is_true=1
                    pck_orders_codes.append(psr_code)
                    break
            if is_true==0:
                print('{0}未生成psr的包裹单'.format(psr_code))
            else:
                is_true = 0
        assert  len(pck_orders_codes) != 0,('全部数据未生成psr包裹单据PCK,{0}'.format(psr_codes))
        return pck_orders_codes

    def update_psr_statue(self,psr_codes):
        sql = """update product_shift_request set request_status=1 where product_shift_request_code in ({0});""".format(list_to_str(psr_codes))
        self.cursor.executeAndcommit(sql)

    def update_pck_statue(self,psr_codes):
        sql = """update package_info set status=0 where is_deleted=0 and order_id in ({0});  """.format(list_to_str(psr_codes))
        self.cursor.executeAndcommit(sql)

    def returnInsertSql(self,psr_code):
        #获取pck主表，并组装插入sql
        psr_codes = list_to_str(psr_code)
        sql = sql_select_pck_info.format(psr_codes)
        pck_main = self.cursor.fetchall(sql)
        pck_main_insert_sql = selectChangeInsert('package_info',pck_main)
        print(pck_main_insert_sql)
        #获取包裹明细表，并组装插入sql
        package_id =  ','.join('\''+str(pck['package_id'])+'\'' for pck in pck_main)
        pck_item = self.cursor.fetchall(sql_select_pck_item.format(package_id))
        pck_item_insert_sql = selectChangeInsert('package_item',pck_item)
        print(pck_item_insert_sql)
        #获取调拨请求
        psr_sql = sql_select_psr.format(psr_codes)
        psr_main = self.cursor.fetchall(psr_sql)
        psr_main_insert_sql = selectChangeInsert('product_shift_request',psr_main)
        print(psr_main_insert_sql)

        #获取调拨请求明细
        psr_ids = ','.join('\''+str(psr['id'])+'\'' for psr in psr_main)
        psr_item = self.cursor.fetchall(sql_select_psr_item.format(psr_ids))
        psr_item_insert_sql = selectChangeInsert('product_shift_request_item',psr_item)
        print(psr_item_insert_sql)
        return pck_main_insert_sql,pck_item_insert_sql,psr_main_insert_sql,psr_item_insert_sql


if __name__=='__main__':
    test = WspPsrSql()
    g= test.returnInsertSql(['PSR-A2-20220311-00674','PSR-A2-20220311-00673'])
    print (g)

