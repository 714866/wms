from django.db import connections
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


class TwmsCommonDB(object):
    def __init__(self):
        self.cursor = mapper.connect_DB('twms_mysql')



def wms_sql_select_return_dict(sql):
    with connections['wms'].cursor() as cursor:
        cursor.execute(sql)
        columns = [info[0]  for info in cursor.description]
        result= [
            dict(zip(columns,row))  for row in cursor.fetchall()
        ]
    return result