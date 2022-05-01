from modular import mapper

find_process_name_by_id = 'select * from ProcessCenter where ProcessCenterID=\'{0}\''


find_oastorage_by_processID='select StorageID,Name from storage where isDefault=1 and Enable=1 and  ProcessCenterID=\'{0}\''

class processSql():
    global find_process_name_by_id


    def __init__(self):
        self.cursor = mapper.connect_sqlserve()

    def findOaProcessNameByID(self, process_id):
        sql = find_process_name_by_id.format(process_id)
        oa_process_name = self.cursor.fetchone(sql)
        return oa_process_name[0]


    def findOaStorageByProcessID(self,process_id):
        sql =find_oastorage_by_processID.format(process_id)
        storage = self.cursor.fetchone(sql)
        return {'storage_id':storage[0],'storage_name':storage[1]}