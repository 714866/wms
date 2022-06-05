from modular.common.commonDB import wmsCommonDB


class PckMessageWMS(wmsCommonDB):
    def PckIsert(self,insert_sqls):
        for insert_sql  in insert_sqls:
            print('插入wms数据'+insert_sql)
            self.cursor.execute(insert_sql)
        self.cursor.commit()