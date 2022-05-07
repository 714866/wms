from modular import mapper
from modular.common.SqlChangeFormat import SqlChangeFormat




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
    def __init__(self):
        self.cursor = mapper.connect_DB()

    def find_source_psr(self,psr_codes):
        sql = self.find_source_psr_sql.format(SqlChangeFormat.list_to_str(psr_codes))
        sql_result = self.cursor.fetchall(sql)
        source_psr_codes = []
        for psr_code in psr_codes:
            for psr_message in sql_result:
                is_true = 0
                if psr_code in psr_message.values():
                    is_true=1
                    source_psr_codes.append(psr_code)
                    break
                print('{0}未生成psr来源单据'.format(psr_code))
        return source_psr_codes
    def find_operation_psr(self,psr_codes):
        '''
        查询psr源单是否生成作业单
        :param psr_codes:
        :return:operation_psr_codes    已生成作业单的调拨单
        '''
        sql = self.find_operation_psr_sql.format(SqlChangeFormat.list_to_str(psr_codes))
        psr_messages = self.cursor.fetchall(sql)
        operation_psr_codes=[]
        for psr_code in psr_codes:
            for psr_message in psr_messages:
                is_true = 0
                if psr_code in psr_message.values():
                    is_true=1
                    operation_psr_codes.append(psr_code)
                    break
                print('{0}未生成psr作业单据'.format(psr_code))
        return operation_psr_codes

    def find_pck_by_psr(self,psr_codes):
        psr_codes = SqlChangeFormat.list_to_str(psr_codes)
        sql = self.find_pck_by_psr_sql.format(psr_codes)
        pck_messages = self.cursor.fetchall(sql)
        pck_orders_codes = []
        for psr_code in psr_codes:
            for psr_message in pck_messages:
                is_true = 0
                if psr_code in psr_message.values():
                    is_true=1
                    pck_orders_codes.append(psr_code)
                    break
                print('{0}未生成psr的包裹单'.format(psr_code))
        return pck_orders_codes



