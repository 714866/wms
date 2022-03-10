from django.db import models

# Create your models here.
class OrderInfo(models.Model):
    oid=models.CharField(max_length=20,primary_key=True)
    user=models.ForeignKey('df_user.UserInfo')
    odate=models.DateTimeField(auto_now_add=True)
    ostatus=models.IntegerField()
    ototal=models.DecimalField(max_digits=10,decimal_places=2)
    oaddress=models.CharField(max_length=100)
    def __str__(self):
        return self.oid.encode('utf-8')

class OrderDetail(models.Model):
    goods=models.ForeignKey('df_goods.GoodsInfo')
    ord=models.ForeignKey('OrderInfo')
    price=models.DecimalField(max_digits=10,decimal_places=2)
    count=models.IntegerField()