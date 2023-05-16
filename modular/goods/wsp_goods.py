from modular.common.commonDB import WspCommonDB
from modular.goods.wsp_sql import get_oa_id_by_pbu, get_oa_id_by_poa, get_oa_id_by_sku


class PsrMessage(WspCommonDB):

    def find_goods_by_oaid(self,sku_oa_id,poa_os_id):
        sql = 'select * from goods_mapper_bg_product where bg_product_id={0} and bg_property_id{1} and is_deleted=0;'.format(sku_oa_id,poa_os_id)
        result = self.cursor.fetchone(sql)
        return result

    def update_goods_delete_date(self):
        for i in range(0,3):
            self.cursor.execute("""update goods set delete_date='1970-01-01 00:00:00' where delete_date=0 limit 200000""")
            self.cursor.commit()
            print(i)


class WspGoods(WspCommonDB):

    def find_goods_by_order_info(self, goods_code):
        goods_code = goods_code.upper()
        if goods_code.startswith('PBU'):
            return self.cursor.fetchone(get_oa_id_by_pbu(goods_code))
        elif goods_code.startswith('POA'):
            return self.cursor.fetchone(get_oa_id_by_poa(goods_code))
        # elif product_code.startwith('SKU'): #则是产品组的,但产品组与SKU是同一个逻辑的，应该合并
        else:
            return self.cursor.fetchone(get_oa_id_by_sku(goods_code))

if __name__=='__main__':
    PsrMessage().update_goods_delete_date()