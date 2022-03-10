#coding=utf-8
#定义乘法技术商品总数，保留两位小数
from django.template import Library

register= Library()

@register.filter()
def mult_c(value,count):
    sum=value*count
    return sum
