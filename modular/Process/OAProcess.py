import time

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

    def findWspProcessId(self,process_id):
        """
        按process_id查询处理中心，返回主表id
        :param process_id:
        :return:
        """
        process_id_sql = """select id from sys_processcenter where processcenter_id={0};""".format(process_id)
        return self.wsp_cursor.fetchone(process_id_sql)['id']

    def updateWspProcessExpand(self,process_id):
        """
        g更新wsp对应处理中心的配置，增加处理中心调拨出库服务
        :param process_id:
        :return:
        """
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

    def insertWspProcessDepartment(self,process_id):
        """
        插入处理中心部门信息
        :param process_id:
        :return:
        """
        now_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        sql = """select id from sys_processcenter_department order by id desc ;"""
        new_id = self.wsp_cursor.fetchone(sql)['id'] + 1
        process_id = self.findWspProcessId(process_id)
        insert_sql = """INSERT INTO wsp.sys_processcenter_department (id, sys_processcenter_id, department_id, create_date, create_user_id,
                                              create_user_name, modify_date, modify_user_id, modify_user_name,
                                              delete_user_id, delete_date, delete_user_name, is_deleted, lock_version,
                                              modify_time_stamp)
VALUES ({0}, {1}, '1a58297bcf64507f9b111473156e9594', '{2}', 1, '开发',
        '{2}', 0, '', 1, '{2}', '开发', 0, 1, '{2}');""".format(new_id,process_id,now_date)
        self.wsp_cursor.executeAndcommit(insert_sql)

    def updateProcessShiftConfige(self,process_id,update_code):

        wsp_process_id = self.findWspProcessId(process_id)
        update_sql = "update sys_processcenter_shift_configuration set {1}=1 where sys_processcenter_id={0}".format(wsp_process_id,update_code)
        self.wsp_cursor.executeAndcommit(update_sql)

if __name__ == "__main__":
    t = processSql()
    t.updateProcessShiftConfige(7,'is_new_goods')