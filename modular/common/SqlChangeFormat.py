"""
各种格式修改成符合sql格式的
"""

class SqlChangeFormat(object):
    def list_to_str(lists):
        sql_str = ''
        for code in lists:
             sql_str+= '\'' + code + '\','
        return sql_str.strip(',')



"""
dumps方法无法对字典中datetime时间格式的数据进行转化
只需重写dumps方法，令其继承json中JSONEncoder类

"""
import json
from datetime import datetime

class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        else:
            return json.JSONEncoder.default(self, obj)

