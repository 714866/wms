

def get_oa_id_by_pbu(pbu):
    return """select distinct gmbp.bg_product_id,gmbp.bg_product_code,gmbp.bg_property_id,gmbp.bg_property_code
from goods g
         inner join goods_mapper_bg_product gmbp on g.id = gmbp.goods_id
where gmbp.is_deleted=0 and g.base_product_code = '{0}';""".format(pbu)


def get_oa_id_by_poa(poa):
    return """select  distinct gmbp.bg_product_id,gmbp.bg_product_code,gmbp.bg_property_id,gmbp.bg_property_code
from goods_mapper_bg_product gmbp where gmbp.bg_property_code='{0}';""".format(poa)

def get_oa_id_by_sku(sku):
    return """select  distinct gmbp.bg_product_id,gmbp.bg_product_code,gmbp.bg_property_id,gmbp.bg_property_code
from goods_mapper_bg_product gmbp where gmbp.bg_product_code='{0}';""".format(sku)