#coding=utf-8
from django.db import models

# Create your models here.
class CartInfo(models.Model):
    use=models.ForeignKey('df_user.UserInfo')
    goods=models.ForeignKey('df_goods.GoodsInfo')
    count=models.IntegerField(default=1)
    # def __str__(self):
    #     return self.goods.encode('utf-8')

