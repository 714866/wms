from modular import mapper

find_process_name_by_id = 'select Name from ProcessCenter where ProcessCenterID=\'{0}\''


find_oastorage_by_processID='select StorageID,Name from storage where isDefault=1 and Enable=1 and  ProcessCenterID=\'{0}\''

class processSql():
    global find_process_name_by_id


    def __init__(self):
        self.cursor = mapper.connect_sqlserve()

    def findOaProcessNameByID(self, process_id):
        sql = find_process_name_by_id.format(process_id)
        oa_process_name = self.cursor.fetchone(sql)
        if oa_process_name is None:
            raise Exception("查询处理中心{0}的为空".format(process_id))
        return oa_process_name['Name']


    def findOaStorageByProcessID(self,process_id):
        sql =find_oastorage_by_processID.format(process_id)
        storage = self.cursor.fetchone(sql)
        if storage is None:
            raise Exception("查询处理中心{0}的店铺为空".format(process_id))
        return {'storage_id':storage['StorageID'],'storage_name':storage['Name']}