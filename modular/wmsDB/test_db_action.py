#c测试SQLAlchemy用的
import os
from configparser import ConfigParser

from modular.wmsDB.model import OdsPckInfo

print(os.path.abspath(os.path.dirname(__file__)))
cp = ConfigParser()
cp.read(os.path.abspath(os.path.dirname(__file__)) + '/../config/mysqldb.conf')
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def connect_dh_alchemy(db_name):
    host = cp.get(db_name, "db_host")
    port = cp.getint(db_name, "db_port")
    user = cp.get(db_name, "db_user")
    password = cp.get(db_name, "db_password")
    database = cp.get(db_name, "db_database")
    db_message = "mysql+pymysql://{user}:{password}@{hostname}:{port}/{database}?charset=utf8".format(user=user,
                                                                                                        password=password,
                                                                                                        hostname=host,
                                                                                                        port=port,
                                                                                                        database=database)
    engine = create_engine(db_message,
                           echo=True,
                           future=True,
                           pool_size=8,   #连接池的大小，默认为5个，设置为0时表示连接无限制
                           pool_recycle=60 * 30,
                           # encoding='utf-8'
                           )  #设置时间以限制数据库多久没连接自动断开
    db_session = sessionmaker(bind=engine)
    return db_session()


def create_ods_info(db_session):

    pass

if __name__=='__main__':
    session = connect_dh_alchemy('wms_mysql')
    ods_info = session.query(OdsPckInfo).filter_by(id=1580950109736501248).all()

    print(ods_info)


