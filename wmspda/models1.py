# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


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
