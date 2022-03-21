from configparser import ConfigParser
import pymysql
import os

print(os.path.abspath(os.path.dirname(__file__)))
cp = ConfigParser()
cp.read(os.path.abspath(os.path.dirname(__file__))+'/config/mysqldb.conf')

# host = cp.get("ods_mysql", "db_host")
# port = cp.getint("ods_mysql", "db_port")
# user = cp.get("ods_mysql", "db_user")
# password = cp.get("ods_mysql", "db_password")
# database = cp.get("ods_mysql", "db_database")

# 打开数据库连接
# db = pymysql.connect(host=host,
#                      port=port,
#                      user=user,
#                      password=password
#                      )
#
# cursor = db.cursor()
#
# cursor.execute("select * from ews.ods_pck_info where package_id='PCK000719080624HJ'")
#
# print(cursor.fetchall())
#
# cursor.close()
# db.close()

def connect_db(db_name):
    host = cp.get(db_name, "db_host")
    port = cp.getint(db_name, "db_port")
    user = cp.get(db_name, "db_user")
    password = cp.get(db_name, "db_password")
    database = cp.get(db_name, "db_database")
    db = pymysql.connect(host=host,
                         port=port,
                         user=user,
                         password=password,
                         database=database
                         )
    return db
