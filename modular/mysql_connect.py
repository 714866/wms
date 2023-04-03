from configparser import ConfigParser
import pymysql
import os

print(os.path.abspath(os.path.dirname(__file__)))
cp = ConfigParser()
cp.read(os.path.abspath(os.path.dirname(__file__)) + '/config/mysqldb.conf')
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

#bit类型查询返回b'\x00 处理
converions = pymysql.converters.conversions
converions[pymysql.FIELD_TYPE.BIT] = lambda x:'0' if 'x00' else '1'

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
                         database=database,
                         cursorclass=pymysql.cursors.DictCursor,
                         conv = converions
                         )
    return db


def connect_dh_alchemy(db_name):
    # alchemy链接
    host = cp.get(db_name, "db_host")
    port = cp.getint(db_name, "db_port")
    user = cp.get(db_name, "db_user")
    password = cp.get(db_name, "db_password")
    database = cp.get(db_name, "db_database")
    db_message = "mysql+pymysql://{user}:{password}@{hostname}/{dbname}:{port}/{database}?charset=utf8".format(user=user,
                                                                                                        password=password,
                                                                                                        hostname=host,
                                                                                                        port=port,
                                                                                                        database=database)
    engine = create_engine("db_message",
                           echo=True,
                           future=True,
                           pool_size=8,   #连接池的大小，默认为5个，设置为0时表示连接无限制
                           pool_recycle=60 * 30)  #设置时间以限制数据库多久没连接自动断开
    return sessionmaker(bind=engine)
    # return db_session
