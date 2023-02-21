#c测试SQLAlchemy用的
import copy
import os
from configparser import ConfigParser

from modular.common.snowID import get_snow_id
from modular.wmsDB.PCK import ods_pck_info_dict, get_ods_pck_info_inser
from modular.wmsDB.model import OdsPckInfo,OdsPckDetail

print(os.path.abspath(os.path.dirname(__file__)))
cp = ConfigParser()
cp.read(os.path.abspath(os.path.dirname(__file__)) + '/../config/mysqldb.conf')
from sqlalchemy import create_engine, select, insert
from sqlalchemy.orm import sessionmaker

def connect_db_alchemy(db_name):
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
    return db_session


def insert_ods_pck_info(db_session):

    pass

if __name__=='__main__':
    Session = connect_db_alchemy('twms_mysql')
    #方法一  定义表对象，新增时对必填项进行添加
    # inser_info = get_ods_pck_info_inser('PCK500142207283525','A00068220718031U',50014)
    # with Session() as session:
    #     session.add(inser_info)
    #     session.commit()

    #方法二：查询后改字段后再插入
    if 1==1:
        inser_ods_pck_detail = select(OdsPckDetail).filter_by(package_id='PCK11072101203D222')
        with Session() as session:
            g = session.execute(inser_ods_pck_detail).fetchone().OdsPckDetail
        c = copy.copy(g)
        g._sa_instance_state.key = None  # 如果判断为
        g.package_id='PCK11072101203D223'
        # OdsPckDetail.insert().returning(g)
        g.id=get_snow_id()

        with Session() as session:
            session.add(g)    # c插入
        # session.execute(insert(OdsPckDetail).values(g))
        # session.commit()
        # ods_info = session.query(OdsPckInfo).filter_by(id=1580950109736501248).all()

        # print(ods_info)


