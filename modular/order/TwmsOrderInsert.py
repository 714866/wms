import time


from modular.common.commonDB import TwmsCommonDB

twms_db=TwmsCommonDB


class TwmsOrderDB(TwmsCommonDB):
    def inser_pck(self,pck,order,process):
        pckInf="""INSERT
        INTO
        twms.ods_pck_info(id, package_id, order_id, batchgridorderdata_id, process_center_id, delivery_type, order_type,
                          detail_type, package_type, batch_processing_id, pck_state, change_state_time, in_ods_date_time,
                          in_wsp_datetime, in_system_datetime, freight, total_price, actual_weight, goods_pck_weight,
                          volume_weight, package_length, package_width, package_height, post_id, post_type_options,
                          online_psot_type, trace_id, way_bill_no, delivery_date, delivery_user_id, delivery_user,
                          receive_name, phone, country_id, country, county, city, buyer_address1, buyer_address2, zip,
                          belonging, belonging_id, pck_remarks, platform_order_id, master_post_no_jump, is_part_delivery,
                          is_gift_lack_delivery, processing_scheme, processing_scheme_remark, return_reason_name,
                          return_reason_remark, create_date, create_user_id, create_user_name, modify_date, modify_user_id,
                          modify_user_name, is_deleted, delete_date, delete_user_id, delete_user_name, modify_time_stamp,
                          lock_version, ods_site_server, init_pck_volume, address, email, in_ods_date_new, real_post_id,
                          payment_type, user_trace_id, cabinet_number, earliest_delivery_date, is_list_scan,
                          deliver_goods_id)
        VALUES({0}, '{1}', '{2}', '', '{3}', ',1,2,3,', 'normal', 3, 3, null, 1,
               '{4}', '{4}', '{4}', '{4}', 0.000, 39.990,
               0.000, 4.300, 0.000, 95.00, 14.00, 14.00, '1815', '1815|0', 'Standard', null, '', '{4}',
               null, null, 'Wallace Krzeminski', '+1 480-618-5344 ext. 22245', '238', 'US', 'New York', 'East Aurora',
               '13325 Schang Road', '', '14052', '516925542164078592', 0, 'TWMS交寄发货主流程错误信息: [对应的库存不存在 ]',
               '113-8470822-7192245', 0, null, null, '', '', '', '', '{4}', 1, '初始化服务', null, 0, '', false,
               null, 0, '', '{4}', 5, '', 18620.000, '13325 Schang Road
        East
        Aurora
        New
        York
        14052
        ', '
        3
        t1rtnnhk0n5jwv @ marketplace.amazon.com
        ', '{4}', '', 0, '', '', '1970-01-01 00:00:00', 0, '1623862545000')"""
        pckDetail="""INSERT INTO twms.ods_pck_detail (id, package_id, item_id, item_name, base_product_name, base_packing_specification,
                                     sale_price, quantity, bar_code_id, sku, poa, bar_code, length, width, height,
                                     goods_spec, goods_attachment_id, item_delivery_weight, goods_manager_name,
                                     sales_user_name, platform_order_id, os_detail_id, transaction_id, create_date,
                                     create_user_id, create_user_name, modify_date, modify_user_id, modify_user_name,
                                     is_deleted, delete_date, delete_user_id, delete_user_name, modify_time_stamp,
                                     lock_version, row, rack, position, is_default, stock_quantity, order_detail_id,
                                     goods_id, bg_product_id, bg_property_id, adapter_num, is_get_rack, area, goods_label)
    VALUES ({itme_id}, '{pck_id}', '59196365780242',
            'KINGSO 3ft x 100ft Weed Barrier Landscape Fabric 5oz Premium Heavy Duty Garden Weed Barrier Fabric High Permeability Woven Weed Gardening Mat Weed Cloth Outdoor Commercial Ground Cover',
            '新SFP产品  新款除草布3*100ft 针刺款', 3, 43.4900, 1, null, '{sku_code}', '{poa_code}', null, 95.00, 14.00, 14.00, '', null,
            4.300, '', '', '', '79572930', 0, '2021-06-16 16:55:46', 1, '初始化服务', null, 0, '', false, null, 0, '',
            '1970-01-02 00:00:00', 0, '', '', '', 0, 0, 623333961, 785934259615555584, 2276935, 0, 0, 1, '', '163,201')"""
        pckAttached="""INSERT INTO twms.ods_pck_attached (id, package_id, order_id, is_repeat_send, is_replenishment, is_split, setting,
                                       original_currency, original_amount, original_ship_fee, original_total_fee,
                                       platform_id, platform_name, store_id, store_name, logistics_account,
                                       order_track_type, region, area, weight_level, is_multi_storage_delivery,
                                       pack_require_id, deficit_price, lights_goods_freight, loss_condition,
                                       jettison_condition, is_cost_control, max_feight, package_service_fee,
                                       package_material_fee, create_date, create_user_id, create_user_name, modify_date,
                                       modify_user_id, modify_user_name, is_deleted, delete_date, delete_user_id,
                                       delete_user_name, modify_time_stamp, lock_version, sales_user_id, sales_user_name,
                                       product_manager_name, product_manager_id, lable_types, requirement_types,
                                       jump_abroad_warehouse_status, is_fulfilled, stock_store_id, mobile_ids)
    VALUES ({0}, '{1}', '{2}', false, false, false, '', 'USD', 39.990, 0.000,
            39.990, '{3}', 'Amazon', '3304', 'Cecvos', '00027', 1, '北美大区', '美西区域', '3', false, null, 0.000, 0.000, '', '', 0,
            0.000, null, 0.500, '2021-06-16 16:55:46', 1, '初始化服务', null, 0, '', false, null, 0, '', '1970-01-02 00:00:00',
            0, 56191, '徐烨沂', '叶华华（重货一组）', 46917, '', '', 0, 0, '3304', '');"""
        ommOrderProcess="""INSERT INTO twms.omm_order_process (id, package_id, order_id, main_post_id, post_id, is_delivery, is_preset, retry_num,
                                        trace_id, link, invoice_url, special_lable_url, waybill_no, freight, weight,
                                        package_type, is_loss, loss_interception_amount, no_loss_interception_amount,
                                        loss_interception_type, loss_factor, loss_value, bargain_interception_type,
                                        has_size_limit, replace_flag, shape, has_master, no_count_limit_post_id,
                                        create_date, create_user_id, create_user_name, modify_date, modify_user_id,
                                        modify_user_name, is_deleted, delete_date, delete_user_id, delete_user_name,
                                        modify_time_stamp, lock_version, error_msg, real_post_id)
    VALUES ({0}, '{1}', '{2}', '689', '689', true, true, 5, 'LZ155547712CN',
            'http://158.85.52.165:7071/file/download?fileUrl=/20210816/844ef1857c05423bbcf5ed6b61fa86c2.PDF', '',
            'http://158.85.52.165:7071/file/download?fileUrl=/20210816/844ef1857c05423bbcf5ed6b61fa86c2.PDF', null, 46.730, 0.442, 'Package', true, 98.89400, 123.90050, 0, 1.000, 85.000, 1, true, true, 0, true, '689',
            '2020-06-14 00:05:09', 1, '', null, 0, '', false, null, 0, '', '2020-08-13 19:53:34', 0, '', '689');"""

        # cursor = self.cursor
        # process=1211
        # process=1142
        pckInfoId=str(time.time()).replace('.','')
        print(pckInf.format(pckInfoId, pck, order,process,time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
        self.cursor.execute(pckInf.format(pckInfoId, pck, order,process,time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
        if process == 1087:
            sku='SKU485329'
            poa='POA1299836'
        elif process!='50025':
            sku ='SKUJ36220'
            poa = 'POA9708319'
        else:
            sku = 'SKUJ36220'
            poa = 'POA9708315'
        pckDetailId=str(time.time()).replace('.','')
        self.cursor.execute(pckDetail.format(itme_id=pckDetailId, pck_id=pck,sku_code=sku,poa_code=poa))

        platform_id='767'
        # 是否需要文件
        is_files= False
        if process==1211 and is_files is False:
            platform_id='766'
        pckAttachedId=str(time.time()).replace('.','',)
        self.cursor.execute(pckAttached.format(pckAttachedId, pck,order,platform_id))
        ommOrderProcessId=str(time.time()).replace('.','')
        self.cursor.execute(ommOrderProcess.format(ommOrderProcessId, pck,order))
        self.cursor.commitAndClose()


if __name__ == "__main__":

    pck='PCK121121061632275'
    order='A000272106150V75'
    # 天马
    process=1221
    # 递四方
    # process=1142
    #海星
    # process=50025
    # 惠州HBA
    process=1087

    start = TwmsOrderDB()
    start.inser_pck(pck,order,process)