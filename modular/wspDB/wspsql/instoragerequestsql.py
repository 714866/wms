sql_get_instorage_request_by_customer = """
select *
from in_storage_request where customer_order_no in ({customer_order_no}) and is_deleted=0;
"""


sql_update_isr_request_sr_status="""

update in_storage_request set sr_status=1 where is_deleted=0 and customer_order_no in ({customer_order_no})
"""


sql_select_isr_request="""
select id,
       in_storage_request_no,
       customer_order_no,
       owner_id,
       manager_id,
       processcenter_id,
       target_processcenter_id,
       global_order_code,
       package_quantity,
       goods_quantity,
       all_weight,
       all_volume,
       pickup_way,
       pickup_adress,
       pickup_date,
       pickup_time,
       delivery_channels,
       shipment_number,
       sr_type,
       sr_status,
       is_stick_label,
       ship_type,
       bol_Number,
       cabinet_Number,
       remark,
       origin_system_type,
       origin_type,
       create_date,
       create_user_id,
       create_user_name,
       modify_user_id,
       modify_user_name,
       modify_date,
       lock_version,
       modify_time_stamp,
       is_deleted,
       delete_user_id,
       delete_user_name,
       delete_date,
       lcl_limit_level,
       storage_code,
       is_charged,
       is_liquid,
       is_powder_past,
       delivery_product_code,
       amazon_shop,
       goods_type,
       sign_user_id,
       sign_date,
       related_code,
       trace_code,
       is_customs,
       audit_status,
       store_type,
       is_drowback,
       shipment_id,
       is_vacuum_packing,
       is_inspection_completed,
       is_shift_costing,
       owner_name,
       goods_size,
       origin_processcenter_id
from in_storage_request where customer_order_no in ({customer_order_no}) and is_deleted=0;"""


sql_select_isr_box="""select id,
       in_storage_request_id,
       box_code,
       weight,
       length,
       width,
       height,
       sort,
       create_date,
       create_user_id,
       create_user_name,
       modify_user_id,
       modify_user_name,
       modify_date,
       is_deleted,
       lock_version,
       modify_time_stamp,
       status,
       complete_date,
       is_full,
       customer_box_code
from in_storage_request_box where is_deleted=0 and in_storage_request_id in ({in_storage_request_id});"""


sql_select_isr_box_item="""select id,
       isr_box_id,
       goods_id,
       produce_info_id,
       batch_code,
       generate_date,
       effective_date,
       plan_receipt_quantity,
       pending_receipt_quantity,
       received_receipt_quantity,
       is_new,
       sampling_ratio,
       is_quality_inspection,
       inspection_remark,
       sort,
       create_date,
       create_user_id,
       create_user_name,
       modify_date,
       modify_user_id,
       modify_user_name,
       is_deleted,
       lock_version,
       modify_time_stamp,
       exception_quantity,
       is_abnormal,
       origin_code,
       external_code,
       sale_platform,
       speed,
       is_first_order
from in_storage_request_box_item where is_deleted=0 and isr_box_id in ({isr_box_id});
"""