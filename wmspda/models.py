# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
import sqlalchemy

class OdsPckInfo(models.Model):
    id = models.BigIntegerField(primary_key=True)
    package_id = models.CharField(max_length=20)
    order_id = models.CharField(max_length=30)
    # batchgridorderdata_id = models.CharField(max_length=30)  # wsp没有这个字段，
    process_center_id = models.IntegerField()
    delivery_type = models.CharField(max_length=50)
    order_type = models.CharField(max_length=20, blank=True, null=True)
    detail_type = models.IntegerField(blank=True, null=True)
    package_type = models.IntegerField(blank=True, null=True)
    batch_processing_id = models.CharField(max_length=50, blank=True, null=True)
    pck_state = models.IntegerField(blank=True, null=True)
    change_state_time = models.DateTimeField(blank=True, null=True)
    in_ods_date_time = models.DateTimeField()
    in_wsp_datetime = models.DateTimeField(blank=True, null=True)
    in_system_datetime = models.DateTimeField(blank=True, null=True)
    freight = models.DecimalField(max_digits=18, decimal_places=3, blank=True, null=True)
    total_price = models.DecimalField(max_digits=18, decimal_places=3, blank=True, null=True)
    actual_weight = models.DecimalField(max_digits=9, decimal_places=3, blank=True, null=True)
    goods_pck_weight = models.DecimalField(max_digits=9, decimal_places=3, blank=True, null=True)
    volume_weight = models.DecimalField(max_digits=9, decimal_places=3, blank=True, null=True)
    package_length = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
    package_width = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
    package_height = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
    post_id = models.CharField(max_length=11, blank=True, null=True)
    post_type_options = models.CharField(max_length=1000, blank=True, null=True)
    online_psot_type = models.CharField(max_length=100, blank=True, null=True)
    trace_id = models.CharField(max_length=80, blank=True, null=True)
    way_bill_no = models.CharField(max_length=80)
    delivery_date = models.DateTimeField(blank=True, null=True)
    delivery_user_id = models.IntegerField(blank=True, null=True)
    delivery_user = models.CharField(max_length=20, blank=True, null=True)
    receive_name = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    country_id = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=300, blank=True, null=True)
    county = models.CharField(max_length=300, blank=True, null=True)
    city = models.CharField(max_length=300, blank=True, null=True)
    buyer_address1 = models.CharField(max_length=300, blank=True, null=True)
    buyer_address2 = models.CharField(max_length=300, blank=True, null=True)
    zip = models.CharField(max_length=150, blank=True, null=True)
    belonging = models.CharField(max_length=20, blank=True, null=True)
    belonging_id = models.IntegerField()
    pck_remarks = models.CharField(max_length=800, blank=True, null=True)
    platform_order_id = models.CharField(max_length=50, blank=True, null=True)
    master_post_no_jump = models.IntegerField(blank=True, null=True)
    is_part_delivery = models.TextField(blank=True, null=True)  # This field type is a guess.
    is_gift_lack_delivery = models.TextField(blank=True, null=True)  # This field type is a guess.
    processing_scheme = models.CharField(max_length=50, blank=True, null=True)
    processing_scheme_remark = models.CharField(max_length=1000, blank=True, null=True)
    return_reason_name = models.CharField(max_length=100, blank=True, null=True)
    return_reason_remark = models.CharField(max_length=1000, blank=True, null=True)
    create_date = models.DateTimeField()
    create_user_id = models.IntegerField()
    create_user_name = models.CharField(max_length=50)
    modify_date = models.DateTimeField(blank=True, null=True)
    modify_user_id = models.IntegerField()
    modify_user_name = models.CharField(max_length=50)
    is_deleted = models.TextField()  # This field type is a guess.
    delete_date = models.DateTimeField(blank=True, null=True)
    delete_user_id = models.IntegerField()
    delete_user_name = models.CharField(max_length=50)
    modify_time_stamp = models.DateTimeField()
    lock_version = models.BigIntegerField()
    ods_site_server = models.CharField(max_length=50, blank=True, null=True)
    init_pck_volume = models.DecimalField(max_digits=20, decimal_places=3)
    address = models.CharField(max_length=300)
    email = models.CharField(max_length=150)
    in_ods_date_new = models.DateTimeField()
    real_post_id = models.CharField(max_length=20)
    payment_type = models.IntegerField()
    user_trace_id = models.CharField(max_length=255)
    cabinet_number = models.CharField(max_length=50, db_collation='utf8mb4_unicode_ci')
    earliest_delivery_date = models.DateTimeField()
    is_list_scan = models.IntegerField()
    deliver_goods_id = models.CharField(max_length=30)
    order_info_json = models.CharField(max_length=2000)
    send_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ods_pck_info'
        app_label = 'wms'

class OdsPckDetail(models.Model):
    id = models.BigIntegerField(primary_key=True)
    package_id = models.CharField(max_length=20)
    item_id = models.CharField(max_length=1000)
    item_name = models.CharField(max_length=800)
    base_product_name = models.CharField(max_length=255)
    base_packing_specification = models.IntegerField()
    sale_price = models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    quantity = models.IntegerField()
    bar_code_id = models.CharField(max_length=50, blank=True, null=True)
    sku = models.CharField(max_length=50)
    poa = models.CharField(max_length=50)
    bar_code = models.CharField(max_length=50, blank=True, null=True)
    length = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
    width = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
    height = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
    goods_spec = models.CharField(max_length=750, blank=True, null=True)
    goods_attachment_id = models.IntegerField(blank=True, null=True)
    item_delivery_weight = models.DecimalField(max_digits=12, decimal_places=3, blank=True, null=True)
    goods_manager_name = models.CharField(max_length=30, blank=True, null=True)
    sales_user_name = models.CharField(max_length=30, blank=True, null=True)
    platform_order_id = models.CharField(max_length=800, blank=True, null=True)
    os_detail_id = models.CharField(max_length=30, blank=True, null=True)
    transaction_id = models.DecimalField(max_digits=18, decimal_places=0, blank=True, null=True)
    create_date = models.DateTimeField()
    create_user_id = models.IntegerField()
    create_user_name = models.CharField(max_length=50)
    modify_date = models.DateTimeField(blank=True, null=True)
    modify_user_id = models.IntegerField()
    modify_user_name = models.CharField(max_length=50)
    is_deleted = models.TextField()  # This field type is a guess.
    delete_date = models.DateTimeField(blank=True, null=True)
    delete_user_id = models.IntegerField()
    delete_user_name = models.CharField(max_length=50)
    modify_time_stamp = models.DateTimeField()
    lock_version = models.BigIntegerField()
    row = models.CharField(max_length=20)
    rack = models.CharField(max_length=20)
    position = models.CharField(max_length=20)
    is_default = models.IntegerField()
    stock_quantity = models.IntegerField()
    order_detail_id = models.BigIntegerField()
    goods_id = models.BigIntegerField()
    bg_product_id = models.IntegerField()
    bg_property_id = models.IntegerField()
    adapter_num = models.IntegerField()
    is_get_rack = models.IntegerField()
    area = models.CharField(max_length=20)
    goods_label = models.CharField(max_length=300, blank=True, null=True)
    order_detail_info_json = models.CharField(max_length=2000)
    category_id_path = models.CharField(max_length=255)
    category_cn_name_path = models.CharField(max_length=255)
    platform_category_id = models.CharField(max_length=255)
    cost_price = models.DecimalField(max_digits=15, decimal_places=4)

    class Meta:
        managed = False
        db_table = 'ods_pck_detail'
        app_label = 'wms'


class OdsPckAttached(models.Model):
    id = models.BigIntegerField(primary_key=True)
    package_id = models.CharField(max_length=20)
    order_id = models.CharField(max_length=30)
    is_repeat_send = models.TextField(blank=True, null=True)  # This field type is a guess.
    is_replenishment = models.TextField(blank=True, null=True)  # This field type is a guess.
    is_split = models.TextField(blank=True, null=True)  # This field type is a guess.
    setting = models.CharField(max_length=50, blank=True, null=True)
    original_currency = models.CharField(max_length=10, blank=True, null=True)
    original_amount = models.DecimalField(max_digits=18, decimal_places=3, blank=True, null=True)
    original_ship_fee = models.DecimalField(max_digits=18, decimal_places=3, blank=True, null=True)
    original_total_fee = models.DecimalField(max_digits=18, decimal_places=3, blank=True, null=True)
    platform_id = models.CharField(max_length=10, blank=True, null=True)
    platform_name = models.CharField(max_length=30)
    store_id = models.CharField(max_length=20, blank=True, null=True)
    store_name = models.CharField(max_length=50)
    logistics_account = models.CharField(max_length=5, blank=True, null=True)
    order_track_type = models.IntegerField(blank=True, null=True)
    region = models.CharField(max_length=50, blank=True, null=True)
    area = models.CharField(max_length=50, blank=True, null=True)
    weight_level = models.CharField(max_length=5, blank=True, null=True)
    is_multi_storage_delivery = models.TextField(blank=True, null=True)  # This field type is a guess.
    pack_require_id = models.CharField(max_length=200, blank=True, null=True)
    deficit_price = models.DecimalField(max_digits=18, decimal_places=3, blank=True, null=True)
    lights_goods_freight = models.DecimalField(max_digits=18, decimal_places=3, blank=True, null=True)
    loss_condition = models.CharField(max_length=100, blank=True, null=True)
    jettison_condition = models.CharField(max_length=100, blank=True, null=True)
    is_cost_control = models.BigIntegerField(blank=True, null=True)
    max_feight = models.DecimalField(max_digits=18, decimal_places=3, blank=True, null=True)
    package_service_fee = models.DecimalField(max_digits=18, decimal_places=3, blank=True, null=True)
    package_material_fee = models.DecimalField(max_digits=18, decimal_places=3, blank=True, null=True)
    create_date = models.DateTimeField()
    create_user_id = models.IntegerField()
    create_user_name = models.CharField(max_length=50)
    modify_date = models.DateTimeField(blank=True, null=True)
    modify_user_id = models.IntegerField()
    modify_user_name = models.CharField(max_length=50)
    is_deleted = models.TextField()  # This field type is a guess.
    delete_date = models.DateTimeField(blank=True, null=True)
    delete_user_id = models.IntegerField()
    delete_user_name = models.CharField(max_length=50)
    modify_time_stamp = models.DateTimeField()
    lock_version = models.BigIntegerField()
    sales_user_id = models.IntegerField(blank=True, null=True)
    sales_user_name = models.CharField(max_length=50, blank=True, null=True)
    product_manager_name = models.CharField(max_length=50, blank=True, null=True)
    product_manager_id = models.IntegerField(blank=True, null=True)
    lable_types = models.CharField(max_length=100)
    requirement_types = models.CharField(max_length=2000)
    jump_abroad_warehouse_status = models.IntegerField()
    is_fulfilled = models.IntegerField()
    stock_store_id = models.CharField(max_length=20)
    mobile_ids = models.CharField(max_length=255, db_collation='utf8mb4_unicode_ci')
    customer_order_type = models.CharField(max_length=20)
    ioss_number = models.CharField(max_length=500)

    class Meta:
        managed = False
        db_table = 'ods_pck_attached'
        app_label = 'wms'


class OdsPckHaikwanDetail(models.Model):
    id = models.BigIntegerField(primary_key=True)
    package_id = models.CharField(max_length=20)
    sku = models.CharField(max_length=50)
    cn_name = models.CharField(max_length=200)
    en_name = models.CharField(max_length=200)
    quantity = models.IntegerField()
    producing_area = models.CharField(max_length=10, blank=True, null=True)
    weight = models.DecimalField(max_digits=9, decimal_places=3)
    currency = models.CharField(max_length=10, blank=True, null=True)
    value = models.DecimalField(max_digits=10, decimal_places=3)
    hscode = models.CharField(max_length=20, blank=True, null=True)
    create_date = models.DateTimeField()
    create_user_id = models.IntegerField()
    create_user_name = models.CharField(max_length=50)
    modify_date = models.DateTimeField(blank=True, null=True)
    modify_user_id = models.IntegerField()
    modify_user_name = models.CharField(max_length=50)
    is_deleted = models.TextField()  # This field type is a guess.
    delete_date = models.DateTimeField(blank=True, null=True)
    delete_user_id = models.IntegerField()
    delete_user_name = models.CharField(max_length=50)
    modify_time_stamp = models.DateTimeField()
    lock_version = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'ods_pck_haikwan_detail'
        app_label = 'wms'


class InStorageRequest(models.Model):
    id = models.BigIntegerField(primary_key=True)
    in_storage_request_no = models.CharField(max_length=30)
    customer_order_no = models.CharField(max_length=50)
    owner_id = models.BigIntegerField()
    manager_id = models.BigIntegerField()
    processcenter_id = models.BigIntegerField()
    target_processcenter_id = models.BigIntegerField()
    global_order_code = models.CharField(max_length=50)
    package_quantity = models.IntegerField()
    goods_quantity = models.IntegerField()
    all_weight = models.DecimalField(max_digits=18, decimal_places=5)
    all_volume = models.DecimalField(max_digits=18, decimal_places=5)
    pickup_way = models.IntegerField()
    pickup_adress = models.CharField(max_length=255)
    pickup_date = models.CharField(max_length=10)
    pickup_time = models.CharField(max_length=20)
    delivery_channels = models.CharField(max_length=30)
    shipment_number = models.CharField(max_length=50)
    sr_type = models.IntegerField()
    sr_status = models.IntegerField()
    is_stick_label = models.IntegerField()
    ship_type = models.IntegerField()
    bol_number = models.CharField(db_column='bol_Number', max_length=50, db_collation='utf8_general_ci')  # Field name made lowercase.
    cabinet_number = models.CharField(db_column='cabinet_Number', max_length=50, db_collation='utf8_general_ci')  # Field name made lowercase.
    remark = models.CharField(max_length=50, db_collation='utf8_general_ci')
    origin_system_type = models.IntegerField()
    origin_type = models.IntegerField()
    create_date = models.DateTimeField()
    create_user_id = models.BigIntegerField()
    create_user_name = models.CharField(max_length=50)
    modify_user_id = models.BigIntegerField()
    modify_user_name = models.CharField(max_length=50)
    modify_date = models.DateTimeField()
    lock_version = models.IntegerField()
    modify_time_stamp = models.DateTimeField()
    is_deleted = models.IntegerField()
    delete_user_id = models.BigIntegerField()
    delete_user_name = models.CharField(max_length=50)
    delete_date = models.DateTimeField()
    lcl_limit_level = models.IntegerField()
    storage_code = models.CharField(max_length=50)
    is_charged = models.IntegerField()
    is_liquid = models.IntegerField()
    is_powder_past = models.IntegerField()
    delivery_product_code = models.CharField(max_length=50)
    amazon_shop = models.CharField(max_length=50)
    goods_type = models.IntegerField()
    sign_user_id = models.BigIntegerField()
    sign_date = models.DateTimeField()
    related_code = models.CharField(max_length=50)
    trace_code = models.CharField(max_length=50)
    is_customs = models.IntegerField()
    audit_status = models.IntegerField()
    store_type = models.IntegerField()
    is_drowback = models.IntegerField()
    shipment_id = models.CharField(max_length=50)
    is_vacuum_packing = models.IntegerField()
    is_inspection_completed = models.IntegerField()
    is_shift_costing = models.IntegerField()
    owner_name = models.CharField(max_length=50)
    goods_size = models.IntegerField()
    origin_processcenter_id = models.BigIntegerField()
    sub_ship_type = models.IntegerField()
    bill_mode = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'in_storage_request'
        app_label = 'wms'


class InStorageRequestBox(models.Model):
    id = models.BigIntegerField(primary_key=True)
    in_storage_request_id = models.BigIntegerField()
    box_code = models.CharField(max_length=50)
    weight = models.DecimalField(max_digits=18, decimal_places=5)
    length = models.DecimalField(max_digits=18, decimal_places=5)
    width = models.DecimalField(max_digits=18, decimal_places=5)
    height = models.DecimalField(max_digits=18, decimal_places=5)
    sort = models.IntegerField()
    create_date = models.DateTimeField()
    create_user_id = models.BigIntegerField()
    create_user_name = models.CharField(max_length=50)
    modify_user_id = models.BigIntegerField()
    modify_user_name = models.CharField(max_length=50)
    modify_date = models.DateTimeField()
    is_deleted = models.IntegerField()
    lock_version = models.IntegerField()
    modify_time_stamp = models.DateTimeField()
    status = models.IntegerField()
    complete_date = models.DateTimeField()
    is_full = models.IntegerField()
    sign_date = models.DateTimeField()
    sign_user_id = models.BigIntegerField()
    customer_box_code = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'in_storage_request_box'
        app_label = 'wms'


class InStorageRequestBoxItem(models.Model):
    id = models.BigIntegerField(primary_key=True)
    isr_box_id = models.BigIntegerField()
    goods_id = models.BigIntegerField()
    produce_info_id = models.CharField(max_length=50)
    batch_code = models.CharField(max_length=100)
    generate_date = models.DateField()
    effective_date = models.DateField()
    plan_receipt_quantity = models.IntegerField()
    pending_receipt_quantity = models.IntegerField()
    received_receipt_quantity = models.IntegerField()
    is_new = models.IntegerField()
    sampling_ratio = models.IntegerField()
    is_quality_inspection = models.IntegerField()
    inspection_remark = models.CharField(max_length=255)
    sort = models.IntegerField()
    create_date = models.DateTimeField()
    create_user_id = models.BigIntegerField()
    create_user_name = models.CharField(max_length=50)
    modify_date = models.DateTimeField()
    modify_user_id = models.BigIntegerField()
    modify_user_name = models.CharField(max_length=50)
    is_deleted = models.IntegerField()
    lock_version = models.IntegerField()
    modify_time_stamp = models.DateTimeField()
    exception_quantity = models.IntegerField()
    is_abnormal = models.IntegerField()
    origin_code = models.CharField(max_length=50)
    external_code = models.CharField(max_length=50)
    sale_platform = models.IntegerField()
    speed = models.CharField(max_length=50)
    wait_confirm_quantity = models.IntegerField()
    hello = models.IntegerField()
    is_first_order = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'in_storage_request_box_item'
        app_label = 'wms'

class Receipt(models.Model):
    id = models.BigIntegerField(primary_key=True)
    receipt_code = models.CharField(max_length=30)
    source_type = models.IntegerField()
    source_code = models.CharField(max_length=30)
    owner_id = models.BigIntegerField()
    manager_id = models.BigIntegerField()
    processcenter_id = models.BigIntegerField()
    target_processcenter_id = models.BigIntegerField()
    is_stick_label = models.IntegerField()
    receipt_status = models.IntegerField()
    ship_type = models.IntegerField()
    in_storage_time = models.DateTimeField()
    create_date = models.DateTimeField()
    create_user_id = models.BigIntegerField()
    create_user_name = models.CharField(max_length=50)
    modify_user_id = models.BigIntegerField()
    modify_user_name = models.CharField(max_length=50)
    modify_date = models.DateTimeField()
    lock_version = models.IntegerField()
    is_full = models.IntegerField()
    sign_date = models.DateTimeField()
    sign_status = models.IntegerField()
    is_deleted = models.IntegerField()
    delete_date = models.DateTimeField()
    delete_user_id = models.BigIntegerField()
    delete_user_name = models.CharField(max_length=50)
    sub_ship_type = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'receipt'
        app_label = 'wms'


class Shelf(models.Model):
    id = models.BigIntegerField(primary_key=True)
    shelf_code = models.CharField(max_length=30)
    source_code = models.CharField(max_length=30)
    source_type = models.IntegerField()
    source_document_type = models.IntegerField()
    source_item_id = models.BigIntegerField()
    goods_id = models.BigIntegerField()
    produce_info_id = models.CharField(max_length=50)
    quantity = models.IntegerField()
    in_quantity = models.IntegerField()
    exception_quantity = models.IntegerField()
    is_abnormal = models.IntegerField()
    remark = models.CharField(max_length=50)
    shelf_status = models.IntegerField()
    owner_id = models.BigIntegerField()
    manager_id = models.BigIntegerField()
    processcenter_id = models.BigIntegerField()
    rack_id = models.BigIntegerField()
    container_code = models.CharField(max_length=30)
    create_date = models.DateTimeField()
    create_user_id = models.BigIntegerField()
    create_user_name = models.CharField(max_length=50)
    modify_user_id = models.BigIntegerField()
    modify_user_name = models.CharField(max_length=50)
    modify_date = models.DateTimeField()
    lock_version = models.IntegerField()
    is_full = models.IntegerField()
    in_storage_box_quantity = models.IntegerField()
    logic_area_id = models.BigIntegerField()
    shelf_rack_id = models.BigIntegerField()
    wait_confirm_quantity = models.IntegerField()
    is_deleted = models.IntegerField()
    delete_date = models.DateTimeField()
    delete_user_id = models.BigIntegerField()
    delete_user_name = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'shelf'
        app_label = 'wms'

class Goods(models.Model):
    id = models.BigIntegerField(primary_key=True)
    base_product_code = models.CharField(max_length=50)
    base_product_name = models.CharField(max_length=255)
    base_product_label = models.CharField(max_length=151)
    base_packing_specification = models.IntegerField()
    base_master_id = models.BigIntegerField()
    default_image = models.CharField(max_length=256)
    storage_attribute = models.CharField(max_length=8)
    is_validity_period = models.CharField(max_length=1)
    status = models.IntegerField()
    auth_status = models.IntegerField()
    information = models.CharField(max_length=255)
    big_packing_quantity = models.IntegerField()
    big_unit = models.CharField(max_length=30)
    small_packing_quantity = models.IntegerField()
    small_unit = models.CharField(max_length=30)
    unit = models.CharField(max_length=10)
    goods_level = models.IntegerField()
    remark = models.CharField(max_length=50)
    storage_condition = models.IntegerField()
    create_user_id = models.IntegerField()
    create_date = models.DateTimeField()
    create_user_name = models.CharField(max_length=20)
    modify_user_id = models.IntegerField()
    modify_date = models.DateTimeField()
    modify_user_name = models.CharField(max_length=20)
    delete_user_id = models.IntegerField()
    delete_date = models.DateTimeField()
    delete_user_name = models.CharField(max_length=20)
    is_deleted = models.IntegerField()
    auth_user_id = models.BigIntegerField()
    auth_date = models.DateTimeField()
    auth_user_name = models.CharField(max_length=20)
    delete_unique_key = models.BigIntegerField()
    lock_version = models.BigIntegerField()
    modify_time_stamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'goods'
        unique_together = (('base_product_code', 'delete_unique_key'),)
        app_label = 'wms'