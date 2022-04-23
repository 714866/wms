from  modular import mapper

find_sku='select * from mafp {0}'

class goodsSql()
    global find_sku
    def __init__(self):
        self.cursor = mapper.connect_sqlserve()
        # updateSql = 'update ProductShiftRequest set bStatus=1 , AuditState=2 where ShiftRequestID in (select top 10 ShiftRequestID from ProductShiftRequest order by ShiftRequestID desc ); '
        newId = cursor.execute(updateSql)

        cursor.commitAndClose()

    def findOaGoodsBySkuu(self,sku_code):

        sql=find_sku.format()
        self.cursor.fetchone()
        pass


