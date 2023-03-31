# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


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
