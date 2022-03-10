#coding=utf-8
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import *
import sys
# sys.path.append('/home/python/python/test1/tiantian/df_user')
# print(sys.path)
from df_user import user_decorator
# Create your views here.

@user_decorator.login
def Cart(request):
    user_id=request.session.get('user_id')
    print(user_id)
    cart_data=CartInfo.objects.filter(use=user_id)
    cart_count=cart_data.count()
    #print(cart_data[0].goods.gpic)
    return render(request,'df_goods/cart.html',{'cart_data':cart_data,'cart_count':cart_count,
                                                'title':'购物车'})




def Cart_handle(request):
    user_ids=request.session.get('user_id')
    good_ids=request.GET['good_id']
    cart_exit = CartInfo.objects.filter(goods_id=good_ids, use_id=user_ids)
    if cart_exit:
        print('已存在')
        cart_exit[0].count+=1
        cart_exit[0].save()
    else:
        cart=CartInfo()
        cart.goods_id=good_ids
        cart.use_id=user_ids

        cart.save()
    return JsonResponse({'answer':'已存入购物车'})

def Cart_delete(request,goods_ids):
    user_ids=request.session.get('user_id')
    cart_exit = CartInfo.objects.filter(goods_id=goods_ids,use_id=user_ids)
    cart_exit[0].delete()
    print('删除成功')
    return JsonResponse({'status':'1'})

def Cart_number(request):
    user_ids=request.session.get('user_id')
    print(user_ids)
    goods_ids=request.GET['goods_id']
    print(goods_ids)
    goods_count=request.GET['count']
    print(goods_count)
    cart_c = CartInfo.objects.get(goods_id=goods_ids,use_id=user_ids)
    print(goods_ids)
    cart_c.count=int(goods_count)
    cart_c.save()
    return JsonResponse({'status':1})

