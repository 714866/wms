


def find_instorage_code_by_relatedcode(code):
    """
    根据入库申请单号、分箱号、来源单号查找收货传递信息
    :param code:
    :return:
    """
    return """select isr.in_storage_request_no,isr.processcenter_id, isrbi.id, isrbi.plan_receipt_quantity, isrbi.goods_id
from in_storage_request isr
         inner join in_storage_request_box isrb on isr.id = isrb.in_storage_request_id
         inner join in_storage_request_box_item isrbi on isrb.id = isrbi.isr_box_id
where isr.in_storage_request_no = '{0}'
   or isr.customer_order_no = '{0}'
   or isrb.box_code = '{0}'""".format(code)

def find_receipt_code(code):

       return """select re.receipt_code,re.processcenter_id
from receipt re
         inner join in_storage_request isr on re.source_code = isr.in_storage_request_no
        inner join in_storage_request_box isrb on isr.id = isrb.in_storage_request_id
where isrb.box_code='{0}' or isr.customer_order_no='{0}'
;""".format(code)



def find_shelf_by_source_code(code,rack):
    return """select s.goods_id, s.quantity - s.in_quantity - s.exception_quantity as quantity, s.source_code, s.shelf_code,'{rack}' as rack 
from shelf s
         inner join in_storage ist on ist.in_storage_no = s.source_code
         inner join receipt r on r.receipt_code = ist.source_code
         inner join in_storage_request isr on isr.in_storage_request_no = r.source_code
         inner join in_storage_request_box isrb on isr.id = isrb.in_storage_request_id
where s.shelf_status=1 and ( isr.in_storage_request_no = '{code}'
   or isr.customer_order_no = '{code}'
   or isrb.box_code = '{code}')
;""".format(code=code,rack=rack)




