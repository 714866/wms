sql_select_pck_info ="""select *
from package_info where is_deleted=0 and order_id in ({0});"""

sql_select_pck_item = """select *
from package_item where is_deleted=0 and  package_id in ({0});"""


sql_select_psr = """select *
from product_shift_request where is_deleted=0 and  product_shift_request_code in ({0});"""

sql_select_psr_item = """select *
from product_shift_request_item where is_deleted=0 and  product_shift_request_id in ({0});"""