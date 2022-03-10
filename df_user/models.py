from django.db import models

class UserInfoManage(models.Manager):
    def get_queryset(self):
        return super(UserInfoManage, self).get_queryset().filter
    def create_info(self,uname,upwd):
        b=UserInfo()
        b.uname=uname
        b.upwd=upwd
        return b

class UserInfo(models.Model):
    uname=models.CharField(max_length=20)
    upwd=models.CharField(max_length=40)
    uemail=models.CharField(max_length=30)
    ushou=models.CharField(max_length=20,default='')
    uaddress=models.CharField(max_length=100,default='')
    uyoubian=models.CharField(max_length=6,default='')
    uphone=models.CharField(max_length=11,default='')

    user1=UserInfoManage()
    user2=models.Manager()

    # def __str__(self):
    #     return self.upwd