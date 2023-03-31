from modular.common.commonDB import WspCommonDB


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

if __name__=='__main__':
    PsrMessage().update_goods_delete_date()