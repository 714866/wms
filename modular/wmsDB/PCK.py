from modular.common.commonDB import wmsCommonDB


ods_pck_info_dict={
    'id':'',
    'package_id':'',
    'order_id':'',
    'batchgridorderdata_id':'',
    'process_center_id':0,
    'delivery_type':'',
    'order_type':'',  #订单类型
    'detail_type':'' , #包裹明细类型
    'package_type':3,  # 包裹类型(文件、信封) WSP计算'
    'batch_processing_id':None,  # 批次号
    'pck_state':1,  #
    'change_state_time':None,  # 状态改变时间
    'in_ods_date_time':None,  #  datetime default CURRENT_TIMESTAMP not null comment '导入ods系统时间戳'
    'in_wsp_datetime':None,  #  导入wsp时间
    'in_system_datetime':None,  #  导入oa时间
    'freight':None,  #  运费
    'total_price':None,  #  订单金额

}



class PckMessageWMS(wmsCommonDB):
    def PckIsert(self,insert_sqls):
        for insert_sql  in insert_sqls:
            print('插入wms数据'+insert_sql)
            self.cursor.execute(insert_sql)
        self.cursor.commit()