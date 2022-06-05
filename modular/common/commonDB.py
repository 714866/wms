from pymysql import IntegrityError

from modular import mapper


class wmsCommonDB(object):
    def __init__(self):
        self.cursor = mapper.connect_DB('wms_mysql')
    def insertLists(self,lists):
        for list  in lists:
            print('插入wms数据'+list)
            try:
                self.cursor.execute(list)
            except IntegrityError as a :
                print("已插入数据{0}".format(list))
        self.cursor.commit()


class WspCommonDB(object):
    def __init__(self):
        self.cursor = mapper.ConnectWSPdb('wsp_mysql')