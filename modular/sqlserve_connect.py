from configparser import ConfigParser
import pymysql
import os
import pymssql


print(os.path.abspath(os.path.dirname(__file__)))
cp = ConfigParser()
cp.read(os.path.abspath(os.path.dirname(__file__))+'/config/mysqldb.conf')
# conn = mssql.connect(host='localhost',
#                      server=r'DESKTOP-3F568LV\MSSQL_INSTANCE',
#                      user='你的登录名',
#                      password='你的密码',
#                      database='你创建好的数据库',
#                      charset='utf8')


def serverConnect_db(db_name="sql_servetest"):
    # database = 'SellerCube'
    # user='skb-test'
    # password='banggood!@#123'

    host = cp.get(db_name, "db_host")
    # port = cp.getint(db_name, "db_port")
    user = cp.get(db_name, "db_user")
    password = cp.get(db_name, "db_password")
    database = cp.get(db_name, "db_database")
    applicationName = "warehouse"
    # server =
    db = pymssql.connect(host, user, password, database)

    return db
