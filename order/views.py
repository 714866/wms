#coding=utf-8
from django.shortcuts import render
from django.http import JsonResponse
import sys
from df_user import user_decorator
from cart.models import *
from df_goods.models import *
from df_user.models import *
from .models import *
from datetime import datetime
from django.db import transaction
# Create your views here.
@user_decorator.login
def order_index(request):
    user_id=request.session.get('user_id')
    good_id=request.GET['good_id']
    total_cart=request.GET['good_total']
    goods_id=good_id.split(',')
    total_cart=total_cart.split(',')
    list=[]
    for i in range(len(goods_id)):
        cart_goods=CartInfo.objects.get(use=user_id,goods=goods_id[i])
        cart_user=UserInfo.user2.get(id=user_id)

        list.append(cart_goods)
    print(list)
    context={"data":list,'use':cart_user}
    return render(request, 'df_goods/place_order.html',context)

@transaction.atomic()  #事务
@user_decorator.login
def order_deal(request):
    user_id=request.session.get('user_id')
    pay=request.POST['total_pay']
    order_id=request.POST.getlist('id[]')
    ux=UserInfo.user2.get(id=user_id)
    print(ux.uaddress)
    add=request.POST.get('address')

    tran_id = transaction.savepoint()  #事务回滚点
    try:
        order=OrderInfo()
        now=datetime.now()
        order.oid = '%s%d'%(now.strftime('%Y%m%d%H%M%S'), user_id)
        order.oaddress=order_id
        order.ototal=pay
        order.ostatus=0
        order.odate=now
        order.user=ux
        order.save()
        for good in order_id:
            cart=CartInfo.objects.get(use=user_id,id=good)
            # goods=GoodsInfo(id=cart.goods.id)
            order_G=OrderInfo.objects.get(oid=order.oid)
            print(cart.count)
            order_detail=OrderDetail()

            order_detail.goods=cart.goods

            order_detail.ord=order_G

            order_detail.price=cart.goods.gprice*cart.count

            order_detail.count=cart.count

            order_detail.save()
            cart.delete()
        return JsonResponse({'status': 1})
    except:
        transaction.savepoint_rollback(tran_id)
        return JsonResponse({'status':0})