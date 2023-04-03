"""
各种格式修改成符合sql格式的
"""
from decimal import Decimal

from pytz import unicode


# class SqlChangeFormat(object):
def list_to_str(lists):
    sql_str = ''
    sql_str = ','.join('\''+str(i)+'\'' for i in lists)
    # for code in lists:
    #      sql_str+= '\'' + code + '\','
    # return sql_str.strip(',')
    return sql_str

def selectChangeInsert(table,select_results):
    """
    将查询返回语句变更为插入语句
    :param table:
    :param select_results:
    :return:
    """
    insert_sql=''
    for select_result in select_results:
        if insert_sql=='':
            row_key = ','.join(str(v) for v in select_result.keys())
            #r如果是类型的 加引号'，不是这不加’
            row_value = ','.join('\'' +str(v) +'\'' if isinstance(v,str) or isinstance(v, unicode) or isinstance(v,datetime) or isinstance(v,date) else str(v) for v in select_result.values())
            row_value = row_value.replace('None', 'NULL')
            insert_sql = "insert into `%s`(%s) values (%s)" % (table, row_key, row_value)
        else:
            row_value = ','.join('\'' +str(v) +'\'' if isinstance(v,str) or isinstance(v, unicode) or isinstance(v,datetime) or isinstance(v,date) else str(v) for v in select_result.values())
            row_value = row_value.replace('None', 'NULL')
            insert_sql = insert_sql + ',(' + row_value + ')'
    return insert_sql

def dict_change_insert(tbale,table_dict):
    """
    传入字段值，返回插入语句
    :param tbale:
    :param table_dict:
    :return:
    """
    pass

"""
dumps方法无法对字典中datetime时间格式的数据进行转化
只需重写dumps方法，令其继承json中JSONEncoder类

"""
import json
from datetime import datetime, date


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


