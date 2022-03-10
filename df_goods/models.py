#coding=utf-8
from django.db import models
from tinymce.models import HTMLField

#商品类型
class TypeInfo(models.Model):
    ttitle=models.CharField(max_length=20)
    isDelete=models.BooleanField(default=False)
    def __str__(self):
        return self.ttitle.encode('utf-8')

#商品
class GoodsInfo(models.Model):
    gtitle=models.CharField(max_length=20)     #名字
    gpic=models.ImageField(upload_to='df_goods')   #图片
    gprice=models.DecimalField(max_digits=5,decimal_places=2)   #价格
    isDelete=models.BooleanField(default=False)
    gunit=models.CharField(max_length=20,default="500g")     #单位
    gclick=models.IntegerField(default=0)         #点击次数
    gjianjie=models.CharField(max_length=200)         #简介
    gkuncun=models.IntegerField()      #库存
    gcontent=HTMLField()             #详情
    gtype=models.ForeignKey('TypeInfo')    #外键对商品类型
    #gadv=models.BooleanField(default=False)
    def __str__(self):
        return self.gtitle.encode('utf-8')

