Frame#coding=utf-8
from django.shortcuts import render
from django.http import JsonResponse
from .models import *
from django.core.paginator import Paginator
from cart.models import CartInfo
import types #查看数据类型
import json

# Create your views here.

#主页
def index(request):
    #获取新鲜水果
    shuiguotype=TypeInfo.objects.get(ttitle="新鲜水果")
    # print(shuiguotype)
    # shuiguo_goods=shuiguotype[0].GoodsInfo_set.all()  #使用GoodsInfo查询不到，只能用goodsinfo
                                                    # ，怀疑是用数据库中的表名
    shuiguo_goods_id=shuiguotype.goodsinfo_set.order_by('-id')[0:4]  #根据id讲4个排序，“-”为降序排
    shuiguo_goods_click=shuiguotype.goodsinfo_set.order_by('-gclick')[0:4] #根据点击量排

    #获取海鲜水产
    seatype=TypeInfo.objects.get(ttitle='海鲜水产')
    sea_goods_id = seatype.goodsinfo_set.order_by('-id')[0:4]
    sea_goods_click = seatype.goodsinfo_set.order_by('-gclick')[0:4]
    # print(sea_goods_id[0].gtitle)

    #获取猪牛羊肉
    meattype=TypeInfo.objects.get(ttitle='猪牛羊肉')
    meat_goods_id = meattype.goodsinfo_set.order_by('-id')[0:4]
    meat_goods_click = meattype.goodsinfo_set.order_by('-gclick')[0:4]
    # print(meat_goods_id[0].gtitle)

    #获取禽类蛋品
    eggstype=TypeInfo.objects.get(ttitle='禽类蛋品')
    eggs_goods_id = eggstype.goodsinfo_set.order_by('-id')[0:4]
    eggs_goods_click = eggstype.goodsinfo_set.order_by('-gclick')[0:4]
    # print(eggs_goods_id[0].gtitle)

    #获取新鲜蔬菜
    vegetablestype=TypeInfo.objects.get(ttitle='新鲜蔬菜')
    vegetables_goods_id = vegetablestype.goodsinfo_set.order_by('-id')[0:4]
    vegetables_goods_click = vegetablestype.goodsinfo_set.order_by('-gclick')[0:4]
    # print(vegetables_goods_id[0].gtitle)

    #获取速冻食品
    foodtype=TypeInfo.objects.get(ttitle='速冻食品')
    food_goods_id = foodtype.goodsinfo_set.order_by('-id')[0:4]
    food_goods_click = foodtype.goodsinfo_set.order_by('-gclick')[0:4]
    # print(food_goods_id[0].gtitle)
    f_type=type(food_goods_id)
    # print(f_type)
    # print('给看下列表')
    context={
        'shuiguo_goods_id':shuiguo_goods_id, 'shuiguo_goods_click':shuiguo_goods_click,
        'sea_goods_id':sea_goods_id, 'sea_goods_click':sea_goods_click,
        'meat_goods_id':meat_goods_id, 'meat_goods_click':meat_goods_click,
        'eggs_goods_id':eggs_goods_id, 'eggshuiguo_goods_ids_goods_click':eggs_goods_click,
        'vegetables_goods_id':vegetables_goods_id, 'vegetables_goods_click':vegetables_goods_click,
        'food_goods_id':food_goods_id, 'food_goods_click':food_goods_click, 'cart_count':cart_count(request),
             }
    return render(request, 'df_goods/index.html', context)


#详情页
def detail(request):
    get=request.GET['id']

    goods=GoodsInfo.objects.get(id=get)
    goods.gclick=goods.gclick+1
    goods.save()
    CartCount=cart_count(request)

    tuijian=GoodsInfo.objects.filter(gtype=goods.gtype).order_by('-id')[0:2]
    context={
        'goods':goods, 'tuijian':tuijian,'cart_count':CartCount,
    }
    response=render(request, 'df_goods/detail.html', context)

    #设置cookie设置浏览记录
    goods_ids=request.COOKIES.get('goods_id','')
    if goods_ids!="":

        list=goods_ids.split(',')
        print(list)
        if get in list:
            list.remove(get)
        list.insert(0, get)
        if len(list)>5:
            list.pop()

        goods_list=','.join(list)
        response.set_cookie('goods_id', goods_list)
    else:
        response.set_cookie('goods_id', get)
    return response



def deal_list(request):
    index=request.GET['deal']
    print(index)
    sort=request.GET['sort'] #获取
    Gype=request.GET['type']
    Type=TypeInfo.objects.get(ttitle=Gype)
    if sort==1:
        goods=GoodsInfo.objects.filter(gtype=Type.id)
    elif sort==2:
        goods=GoodsInfo.objects.filter(gtype=Type.id).order_by('gprice')
    else:
        goods=GoodsInfo.objects.filter(gtype=Type.id).order_by('-gclick')

    Pgoods = Paginator(goods, 10)  # 分页 10个为一页
    Plist = Pgoods.page_range  # 页码列表
    total_pages = Pgoods.count
    goods_list = Pgoods.page(1)  # 第一页

    list=[]

    for a in goods_list.object_list:
        print(type(a.gpic))
        print(type(a.gtitle))
        pic=str(a.gpic)
        print(pic)
        list.append({'gtitle':a.gtitle, 'gpic':pic, 'gprice':a.gprice,'id':a.id})
        print(list[0]['id'])
    return JsonResponse({'js':index,'goods':list})


#列表页
def list(request):
    index=''
    get=request.GET['type']
    Type=TypeInfo.objects.get(ttitle=get)
    goods=GoodsInfo.objects.filter(gtype=Type.id)
    #print(goods[0].gtitle)
    new_goods=Type.goodsinfo_set.order_by('-id')[0:2]
    ren_goods=Type.goodsinfo_set.order_by('-gclick')
    jia_goods=Type.goodsinfo_set.order_by('gprice')
    if index=='':
        index=1
        print(index)
    Pgoods=Paginator(goods,10)       #分页 10个未一页
    Plist=Pgoods.page_range        #页码列表
    total_pages=Pgoods.count
    list=Pgoods.page(index)  #第一页

    Rgoods=Paginator(ren_goods,10)
    Rlist=Rgoods.page(index).object_list

    Jgoods=Paginator(jia_goods,10)
    Jlist=Jgoods.page(index).object_list
    context={
        'goods':goods, 'new_goods':new_goods, 'ren_goods':Rlist, 'jia_goods':Jlist,
        'plist':Plist, 'list':list, 't_pages':total_pages, 'get':get ,'cart_count':cart_count(request)
    }
    return render(request, 'df_goods/list.html', context)

def cart_count(request):
    if request.session.has_key('user_id'):
        return CartInfo.objects.filter(use_id=request.session['user_id']).count()
    else:
        return 0

from haystack.views import SearchView
class MySearchView(SearchView):
    def extra_context(self):
        context=super(MySearchView,self).extra_context()
        context['title']='搜索'
        context['cart_count']=cart_count(self.request)
        return context