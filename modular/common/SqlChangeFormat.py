"""
各种格式修改成符合sql格式的
"""
from decimal import Decimal

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
            """
            只要检查到了是datetime类型的数据就把它转类型
            """
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        elif isinstance(obj, bytes):
            """
            只要检查到了是bytes类型的数据就把它转为str类型
            """
            return str(obj, encoding='utf-8')
        elif isinstance(obj, Decimal):
            """
            只要检查到了是bytes类型的数据就把它转为str类型
            """
            return str(obj)
        else:
            return json.JSONEncoder.default(self, obj)


