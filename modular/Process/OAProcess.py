from modular import mapper

find_process_name_by_id = 'select Name from ProcessCenter where ProcessCenterID=\'{0}\''


find_oastorage_by_processID='select StorageID,Name from storage where isDefault=1 and Enable=1 and  ProcessCenterID=\'{0}\''

class processSql():
    global find_process_name_by_id


    def __init__(self):
        self.cursor = mapper.connect_sqlserve()
        self.wsp_cursor = mapper.ConnectWSPdb()

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

    def updateWspProcessExpand(self,process_id):
        select_sql = ''' select spe.id as id
from sys_processcenter sp
         inner join sys_processcenter_expand spe on spe.sys_processcenter_id = sp.id
where sp.processcenter_id = {0};'''.format(process_id)
        process_expand_id = self.wsp_cursor.fetchone(select_sql)
        assert process_expand_id is not None,'wsp处理中心扩展表sys_processcenter_expand无数据，校验失败'
        update_sql = '''update sys_processcenter_expand
set is_shift_out_stock=1
where id={0}'''.format(process_expand_id['id'])
        # print(update_sql)
        self.wsp_cursor.executeAndcommit(update_sql)

if __name__ == "__main__":
    t = processSql()
    t.updateWspProcessExpand(7)