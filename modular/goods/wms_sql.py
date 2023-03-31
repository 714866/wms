import time

from modular.common.snowID import get_snow_id


def find_not_exict_goods_by_isr_box_id(isr_box_id):
    return """select g.id
from in_storage_request_box_item isrbi
left join goods g on isrbi.goods_id = g.id
where g.id is not  null  and isrbi.isr_box_id={0}""".format(isr_box_id)


def find_isr_goods_id_by_code(code):
    return """select distinct isrbi.goods_id
from in_storage_request isr
         inner join in_storage_request_box isrb on isr.id = isrb.in_storage_request_id
        inner join in_storage_request_box_item isrbi on isrbi.isr_box_id=isrb.id
where  isr.in_storage_request_no='{code}'  or isr.customer_order_no='{code}' or isrb.box_code='{code}' 
;""".format(code=code)


def find_goods_by_id(goods_lists_str):
    return 'select * from goods where id in ({0})'.format(goods_lists_str)


def insert_goods_volume(goods_id, type=2):
    time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    return """INSERT INTO ews.goods_volume (id, goods_id, volume_type, length, width, height, create_user_id, create_date,
                                  create_user_name, modify_user_id, modify_date, modify_user_name, delete_user_id,
                                  delete_date, delete_user_name, is_deleted, delete_unique_key, lock_version)
        VALUES ({id}, {goods_id}, {type}, 10.00000, 10.00000, 10.00000, 1, '{ctime}', 'admin', 0,
            '1970-01-01 00:00:00', '', 0, '1970-01-01 00:00:00', '', false, 0, 0);""".format(id=get_snow_id(),
                                                                                             goods_id=goods_id,
                                                                                             type=type,
                                                                                             ctime=time.strftime(
                                                                                                 "%Y-%m-%d %H:%M:%S",
                                                                                                 time.localtime()))


def inset_goods_weight(goods_id, type=2):
    return """INSERT INTO ews.goods_weight (id, goods_id, weight_type, weight, create_user_id, create_date, create_user_name,
                              modify_user_id, modify_date, modify_user_name, delete_user_id, delete_date,
                              delete_user_name, is_deleted, delete_unique_key, lock_version)
VALUES ({id}, {goods_id}, {weight_type}, 210.00000, 1, '{ctime}', 'admin', 0,
        '1970-01-01 00:00:00', '', 0, '1970-01-01 00:00:00', '', false, 0, 0);""".format(id=get_snow_id(),
                                                                                         goods_id=goods_id,
                                                                                         weight_type=type,
                                                                                         ctime=time.strftime(
                                                                                             "%Y-%m-%d %H:%M:%S",
                                                                                             time.localtime()))


def goods_weight_not_exict(goods_id):
    return """select  goods_id  from goods_weight where goods_id in ({0}) and is_deleted=0 and weight_type=2  """.format(
        goods_id)


def goods_volume_not_exict(goods_id):
    return """select  goods_id  from goods_volume where goods_id in ({0}) and is_deleted=0 and volume_type=2  """.format(
        goods_id)


def goods_weight_exist_zero(goods_id):
    return """select  id  from goods_weight where weight=0 and goods_id in ({0}) """.format(goods_id)


def goods_volume_exist_zero(goods_id):
    return """select id,length,width,height from goods_volume where goods_id in ({0}) and (length=0 or width=0 or height=0 )""".format(
        goods_id)


def update_goods_weight_valuse(id, valuse):
    return """update goods_weight set weight={0} where id in ({1})""".format(valuse, id)


def update_goods_volume_valuse(id, valuse):
    return """update goods_volume set length={0},width={0},height={0} where id in ({1})""".format(valuse, id)
