# coding: utf-8
from sqlalchemy import *
from sqlalchemy.dialects.mysql.types import _IntegerType, _StringType
from sqlalchemy.dialects.postgresql import BIT
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class OdsPckInfo(Base):
    __tablename__ = 'ods_pck_info'
    __table_args__ = (
        Index('idx_process_center_id', 'process_center_id', 'in_ods_date_time', 'pck_state'),
        Index('idx_pck_state_is_deleted', 'pck_state', 'is_deleted')
    )

    id = Column(_IntegerType(20), primary_key=True)
    package_id = Column(_StringType(20), nullable=False, index=True)
    order_id = Column(_StringType(20), nullable=False, index=True, server_default="''")
    batchgridorderdata_id = Column(_StringType(30), nullable=False, index=True, server_default="''")
    process_center_id = Column(_IntegerType(11), nullable=False, server_default="'0'")
    delivery_type = Column(_StringType(50), nullable=False, server_default="''")
    order_type = Column(_StringType(20))
    detail_type = Column(_IntegerType(11))
    package_type = Column(_IntegerType(11))
    batch_processing_id = Column(_StringType(50), index=True)
    pck_state = Column(_IntegerType(11))
    change_state_time = Column(DateTime)
    in_ods_date_time = Column(DateTime, nullable=False, server_default='CURRENT_TIMESTAMP')
    in_wsp_datetime = Column(DateTime)
    in_system_datetime = Column(DateTime)
    freight = Column(DECIMAL(18, 3))
    total_price = Column(DECIMAL(18, 3))
    actual_weight = Column(DECIMAL(9, 3))
    goods_pck_weight = Column(DECIMAL(9, 3), server_default="'0.000'")
    volume_weight = Column(DECIMAL(9, 3), server_default="'0.000'")
    package_length = Column(DECIMAL(9, 2), server_default="'0.00'")
    package_width = Column(DECIMAL(9, 2), server_default="'0.00'")
    package_height = Column(DECIMAL(9, 2), server_default="'0.00'")
    post_id = Column(_StringType(11), index=True)
    post_type_options = Column(_StringType(1000))
    online_psot_type = Column(_StringType(100))
    trace_id = Column(_StringType(80), index=True)
    way_bill_no = Column(_StringType(80), nullable=False, index=True, server_default="''")
    delivery_date = Column(DateTime, index=True)
    delivery_user_id = Column(_IntegerType(11))
    delivery_user = Column(_StringType(20), index=True)
    receive_name = Column(_StringType(100))
    phone = Column(_StringType(50))
    country_id = Column(_StringType(20), index=True)
    country = Column(_StringType(300))
    county = Column(_StringType(300))
    city = Column(_StringType(300))
    buyer_address1 = Column(_StringType(300))
    buyer_address2 = Column(_StringType(300))
    zip = Column(_StringType(150))
    belonging = Column(_StringType(20))
    belonging_id = Column(_IntegerType(2), nullable=False, server_default="'0'")
    pck_remarks = Column(_StringType(800))
    platform_order_id = Column(_StringType(50))
    master_post_no_jump = Column(_IntegerType(1))
    is_part_delivery = Column(BIT(1))
    is_gift_lack_delivery = Column(BIT(1))
    processing_scheme = Column(_StringType(50))
    processing_scheme_remark = Column(_StringType(1000))
    return_reason_name = Column(_StringType(100))
    return_reason_remark = Column(_StringType(1000))
    create_date = Column(DateTime, nullable=False, index=True)
    create_user_id = Column(_IntegerType(11), nullable=False, server_default="'0'")
    create_user_name = Column(_StringType(50), nullable=False, server_default="''")
    modify_date = Column(DateTime)
    modify_user_id = Column(_IntegerType(11), nullable=False, server_default="'0'")
    modify_user_name = Column(_StringType(50), nullable=False, server_default="''")
    is_deleted = Column(BIT(1), nullable=False)
    delete_date = Column(DateTime)
    delete_user_id = Column(_IntegerType(11), nullable=False, server_default="'0'")
    delete_user_name = Column(_StringType(50), nullable=False, server_default="''")
    modify_time_stamp = Column(DateTime, nullable=False, index=True, server_default='CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP')
    lock_version = Column(_IntegerType(20), nullable=False, server_default="'0'")
    ods_site_server = Column(_StringType(50))
    init_pck_volume = Column(DECIMAL(20, 3), server_default="'0.000'")
    address = Column(_StringType(300), nullable=False, server_default="''")
    email = Column(_StringType(150), nullable=False, server_default="''")
    in_ods_date_new = Column(DateTime, nullable=False, server_default='CURRENT_TIMESTAMP')
    payment_type = Column(_IntegerType(4), nullable=False, server_default="'1'")
    user_trace_id = Column(_StringType(255), nullable=False, server_default="''")
    real_post_id = Column(_StringType(20), nullable=False, server_default="''")
    cabinet_number = Column(_StringType(50), nullable=False, server_default="''")
    earliest_delivery_date = Column(DateTime, nullable=False, server_default="'1970-01-01 00:00:00'")
    is_list_scan = Column(_IntegerType(1), nullable=False, server_default="'0'")
    deliver_goods_id = Column(_StringType(30), nullable=False, server_default="''")
    distribution_complete_date = Column(DateTime, nullable=False, server_default="'1970-01-01 00:00:00'")
    order_info_json = Column(_StringType(2000), nullable=False, server_default="''")
    send_date = Column(DateTime, nullable=False, server_default="'1970-01-01 00:00:00'")
    container_code = Column(_StringType(50), nullable=False, index=True, server_default="''")
