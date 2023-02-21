import time

from modular.common.commonDB import wmsCommonDB
from modular.common.snowID import get_snow_id

ods_pck_info_dict={
    'id':get_snow_id(),
    'package_id':'PCK500142207283523',
    'order_id':'A00068220718029U',
    # 'batchgridorderdata_id':50014,
    'process_center_id':50014,
    'delivery_type':'1,2,3',
    'order_type':'normal',  #订单类型
    'detail_type':'' , #包裹明细类型
    'package_type':3,  # 包裹类型(文件、信封) WSP计算'
    'batch_processing_id':None,  # 批次号
    'pck_state':1,  #
    'change_state_time':None,  # 状态改变时间
    'in_ods_date_time':None,  #  datetime default CURRENT_TIMESTAMP not null comment '导入ods系统时间戳'
    'in_wsp_datetime':None,  #  导入wsp时间
    'in_system_datetime':None,  #  导入oa时间
    'freight':0.000,  #  运费
    'total_price':39.990,  #  订单金额
    'actual_weight':0.000, #实际金额
    'goods_pck_weight':39.990, #商品包裹重量
    'volume_weight':None, #计抛体积重量
    'package_length':95.00, #包裹长
    'package_width':14.00, #包裹宽
    'package_height':14.00, #包裹宽
    'post_id':1815, #渠道id
    'post_type_options':'1815|0', #渠道id
    'online_psot_type':'Standard', #在线邮寄方式
    'trace_id':None, #跟踪号
    'way_bill_no':None, #中转单号
    'delivery_date':None, #交寄时间
    'delivery_user_id':None, #交寄人
    'receive_name':'Wallace Krzeminski', #收件人姓名
    'phone':'0422634606', #收件人电话
    'country_id':'13', #国家ID
    'country':'DE', #国家名称
    'county':'Victoria', #省
    'city':'Croydon North', #城市
    'buyer_address1':'4 Hurst Court', #地址1
    'buyer_address2':None, #地址2
    'zip':14052, #邮编
    'belonging':0, #开发平台  0棒谷 1yoms
    'pck_remarks':None, #备注
    'platform_order_id':'24-05439-22494', #平台原始单号
    'master_post_no_jump':0, #主邮不跳转
    'is_part_delivery':None, #是否部分发货
    'is_gift_lack_delivery':0, #赠品缺货是否发货
    'processing_scheme':None, #
    'processing_scheme_remark':None, #
    'return_reason_name':None, #
    'return_reason_remark':None, #
    'return_reason_remark':None, #
    'create_date':  time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),#创建时间
    'create_user_id':1,#创建人id
    'create_user_name':'初始化服务',#创建人
    'modify_date':None,#修改时间
    'modify_user_id':'0',#修改人
    'modify_user_name':'',#修改人
    'is_deleted':0,
    'delete_user_id':'0',#
    'delete_user_name':'',#
    'modify_time_stamp':'',# 可注释
    'lock_version':'0',# 可注释
    'ods_site_server':'',# 可注释
    'init_pck_volume':'18620.000',# 可注释
    'address':'13325 Schang Road',# 地址
    'email':'ange.formston@gmail.com',# 邮件
    'in_ods_date_new':None,# 时间
    'real_post_id':'',# 实际交寄
    'payment_type':0,# 实际交寄 可注释
    'user_trace_id':0,# 用户跟踪号 可注释

}



# real_post_id = Column(_StringType(20), nullable=False, server_default="''")
# payment_type = Column(_IntegerType(4), nullable=False, server_default="'1'")
# user_trace_id = Column(_StringType(255), nullable=False, server_default="''")
# cabinet_number = Column(_StringType(50), nullable=False, server_default="''")
# earliest_delivery_date = Column(DateTime, nullable=False, server_default="'1970-01-01 00:00:00'")
# is_list_scan = Column(_IntegerType(1), nullable=False, server_default="'0'")
# deliver_goods_id = Column(_StringType(30), nullable=False, server_default="''")
# order_info_json = Column(_StringType(2000), nullable=False, server_default="''")
# send_date = Column(DateTime)
from modular.wmsDB.model import OdsPckInfo
def get_ods_pck_info_inser(pck_code,order_code,process_id):
    return OdsPckInfo(
        id=get_snow_id(),
        # package_id='PCK500142207283524',
        # order_id='A00068220718030U',
        package_id=pck_code,
        order_id=order_code,
        batchgridorderdata_id=50014,
        # process_center_id=50014,
        process_center_id=process_id,
        delivery_type='1,2,3',
        order_type='normal',  #订单类型
        detail_type='1' , #包裹明细类型
        package_type=3,  # 包裹类型(文件、信封) WSP计算'
        batch_processing_id=None,  # 批次号
        pck_state=1,  #
        change_state_time=None,  # 状态改变时间
        in_ods_date_time=None,  #  datetime default CURRENT_TIMESTAMP not null comment '导入ods系统时间戳'
        in_wsp_datetime=None,  #  导入wsp时间
        in_system_datetime=None,  #  导入oa时间
        freight=0.000,  #  运费
        total_price=39.990,  #  订单金额
        actual_weight=0.000, #实际金额
        goods_pck_weight=39.990, #商品包裹重量
        volume_weight=None, #计抛体积重量
        package_length=95.00, #包裹长
        package_width=14.00, #包裹宽
        package_height=14.00, #包裹宽
        post_id=1815, #渠道id
        post_type_options='1815|0', #渠道id
        online_psot_type='Standard', #在线邮寄方式
        trace_id=None, #跟踪号
        way_bill_no=None, #中转单号
        delivery_date=None, #交寄时间
        delivery_user_id=None, #交寄人
        receive_name='Wallace Krzeminski', #收件人姓名
        phone='0422634606', #收件人电话
        country_id='13', #国家ID
        country='DE', #国家名称
        county='Victoria', #省
        city='Croydon North', #城市
        buyer_address1='4 Hurst Court', #地址1
        buyer_address2=None, #地址2
        zip=14052, #邮编
        belonging=0, #开发平台  0棒谷 1yoms
        pck_remarks=None, #备注
        platform_order_id='24-05439-22494', #平台原始单号
        master_post_no_jump=0, #主邮不跳转
        is_part_delivery=None, #是否部分发货
        is_gift_lack_delivery=0, #赠品缺货是否发货
        processing_scheme=None, #
        processing_scheme_remark=None, #
        return_reason_name=None, #
        return_reason_remark=None, #
        create_date= time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),#创建时间
        create_user_id=1,#创建人id
        create_user_name='初始化服务',#创建人
        # modify_date=None,#修改时间  有默认值，使用none就无法使用默认值了
        modify_user_id='0',#修改人
        modify_user_name='',#修改人
        is_deleted=0,
        delete_user_id='0',#
        delete_user_name='',#
        # modify_time_stamp='',# 可注释
        lock_version='0',# 可注释
        ods_site_server='',# 可注释
        init_pck_volume='18620.000',# 可注释
        address='13325 Schang Road',# 地址
        email='ange.formston@gmail.com',# 邮件
        in_ods_date_new=None,# 时间
        real_post_id='',# 实际交寄
        payment_type=0,# 实际交寄 可注释
        user_trace_id=0# 用户跟踪号 可注释
    )

# def get_ods_pck_detai(package_code,order_code):
#     id = get_snow_id()
#     package_id = package_code,
#     order_id = order_code,
#     is_repeat_send = Column(BIT(1))
#     is_replenishment = Column(BIT(1))
#     is_split = Column(BIT(1))
#     setting = Column(_StringType(50))
#     original_currency = Column(_StringType(10))
#     original_amount = Column(DECIMAL(18, 3))
#     original_ship_fee = Column(DECIMAL(18, 3))
#     original_total_fee = Column(DECIMAL(18, 3))
#     platform_id = Column(_StringType(10))
#     platform_name = Column(_StringType(30), nullable=False, server_default="''")
#     store_id = Column(_StringType(20))
#     store_name = Column(_StringType(50), nullable=False, server_default="''")
#     logistics_account = Column(_StringType(5))
#     order_track_type = Column(_IntegerType(11))
#     region = Column(_StringType(50))
#     area = Column(_StringType(50))
#     weight_level = Column(_StringType(5))
#     is_multi_storage_delivery = Column(BIT(1))
#     pack_require_id = Column(_StringType(200))
#     deficit_price = Column(DECIMAL(18, 3))
#     lights_goods_freight = Column(DECIMAL(18, 3))
#     loss_condition = Column(_StringType(100))
#     jettison_condition = Column(_StringType(100))
#     is_cost_control = Column(_IntegerType(20))
#     max_feight = Column(DECIMAL(18, 3))
#     package_service_fee = Column(DECIMAL(18, 3))
#     package_material_fee = Column(DECIMAL(18, 3))
#     create_date = Column(DateTime, nullable=False, index=True)
#     create_user_id = Column(_IntegerType(11), nullable=False, server_default="'0'")
#     create_user_name = Column(_StringType(50), nullable=False, server_default="''")
#     modify_date = Column(DateTime)
#     modify_user_id = Column(_IntegerType(11), nullable=False, server_default="'0'")
#     modify_user_name = Column(_StringType(50), nullable=False, server_default="''")
#     is_deleted = Column(BIT(1), nullable=False)
#     delete_date = Column(DateTime)
#     delete_user_id = Column(_IntegerType(11), nullable=False, server_default="'0'")
#     delete_user_name = Column(_StringType(50), nullable=False, server_default="''")
#     modify_time_stamp = Column(DateTime, nullable=False, index=True, server_default="'1970-01-02 00:00:00'")
#     lock_version = Column(_IntegerType(20), nullable=False, server_default="'0'")
#     sales_user_id = Column(_IntegerType(11), server_default="'0'")
#     sales_user_name = Column(_StringType(50))
#     product_manager_name = Column(_StringType(50))
#     product_manager_id = Column(_IntegerType(11), server_default="'0'")
#     lable_types = Column(_StringType(100), nullable=False, server_default="''")
#     requirement_types = Column(_StringType(2000), nullable=False, server_default="''")
#     jump_abroad_warehouse_status = Column(_IntegerType(4), nullable=False, server_default="'0'")
#     is_fulfilled = Column(_IntegerType(1), nullable=False, server_default="'0'")
#     stock_store_id = Column(_StringType(20), nullable=False, server_default="''")
#     mobile_ids = Column(_StringType(255), nullable=False, server_default="''")
#     customer_order_type = Column(_StringType(20), nullable=False, server_default="''")
#     ioss_number = Column(_StringType(500), nullable=False, server_default="''")

class PckMessageWMS(wmsCommonDB):
    def PckIsert(self,insert_sqls):
        for insert_sql  in insert_sqls:
            print('插入wms数据'+insert_sql)
            self.cursor.execute(insert_sql)
        self.cursor.commit()