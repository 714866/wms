#coding=utf-8
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from .models import *
from hashlib import sha1
from . import user_decorator
from order.models import *
from df_goods.models import *
from django.core.paginator import Paginator


#创建账号
def register(request):
    return render(request, 'df_user/register.html')
# 判断用户是否存在
def register_exit(request):
    print("abcd")
    get_name=request.GET['uname']
    c=UserInfo.user2.filter(uname=get_name)
    COUNT=c.count()
    return JsonResponse({'count':COUNT})

#验证
def register_handle(request):
    # return HttpResponse("detail" )
    post=request.POST
    uname=post.get("user_name")
    upassword=post.get("pwd")
    ucpassword=post.get("cpwd")
    uemail=post.get("email")
    if upassword!=ucpassword:
        return redirect("/user/register/")
    #加密
    s1=sha1()
    s1.update(upassword)
    upwd3=s1.hexdigest()

    user=UserInfo()
    user.uname=uname
    user.upwd=upwd3
    user.uemail=uemail
    user.save()
    return redirect('/user/login/')

#登陆页面
def login(request):
    # post=request.POST
    # uname=post.get('username')
    # upwd=post.get('pwd')
    # return render(request, 'df_user/login.html')
    #自己写的
    uname=request.COOKIES.get('uname','')
    error_name=request.COOKIES.get('error_name',0)
    error_pwd=request.COOKIES.get('error_pwd',0)
    context={
        'title':'登陆名','error_name':error_name,'error_pwd':error_pwd,'uname':uname
    }
    return render(request,'df_user/login.html',context)






#登录处理
# def login_handl(request):
#     post=request.POST
#     getusername=post.get('username')
#     getpwd=post.get('pwd')
#     getjizhu=post.get('jizhu',0)
#     s2=sha1()
#     s2.update(getpwd)
#     s_upd=s2.hexdigest()
#     user=UserInfo.user2.filter(uname=getusername)
#     if user[0].upwd==s_upd:
#         return redirect('/user/user_center_info/')
#     else:
#         return HttpResponse('登陆失败')
#     # return redirect('/usr/user_center_info/')
#自己写的
def login_handl(request):
    post=request.POST
    getusername=post.get('username')
    getpwd=post.get('pwd')
    getjizhu=post.get('jizhu', 0)
    user = UserInfo.user2.filter(uname=getusername)
    if len(user)==1:
        s2=sha1()
        s2.update(getpwd)
        s_upd=s2.hexdigest()

        if user[0].upwd==s_upd:
            url=request.COOKIES.get('url','/user/user_center_info')
            red=HttpResponseRedirect(url)
            if getjizhu!=0:
                red.set_cookie('uname', getusername)
                red.set_cookie('error_name', 0)
                red.set_cookie('error_pwd', 0)
            else:
                red.set_cookie('uname', '', max_age=-1)
            request.session['user_name']=getusername
            request.session['user_id']=user[0].id
            return red
        else:
            red=HttpResponseRedirect('/user/login/')
            red.set_cookie('title', '用户登陆1')
            red.set_cookie('error_name', 0)
            red.set_cookie('error_pwd', 1)
            red.set_cookie('uname', getusername)
            return red
    #         context = {'title':'用户登陆1','error_name':0,'error_pwd':1,'uname':getusername}
    #         return render(request,'df_user/login.html',context)
    else:
        red = HttpResponseRedirect('/user/login')
        red.set_cookie('title', '用户登陆1')
        red.set_cookie('error_name', 1)
        red.set_cookie('error_pwd', 0)
        red.set_cookie('uname', getusername)
        return red

    # return redirect('/usr/user_center_info/')


@user_decorator.login
def user_center_info(request):
    user_name=request.session.get('user_name')
    goods_ids = request.COOKIES.get('goods_id', '') #储存浏览商品的goods_id
    goods=[]
    if goods_ids!='':
        list=goods_ids.split(',')
        for i in list:
            g=GoodsInfo.objects.get(id=1)
            goods.append(GoodsInfo.objects.get(id=i))


    user = UserInfo.user2.get(uname=user_name)

    context={'title':'用户中心', 'user_name':user_name, 'user':user, 'goods':goods}
    return render(request, "df_user/user_center_info.html", context)

@user_decorator.login
def user_center_order(request):
    user_name=request.session.get('user_name')
    user_id=request.session.get('user_id')
    order=OrderInfo.objects.filter(user=user_id).order_by('-oid')
    Page=Paginator(order,2)
    total_pages=Page.count
    list=Page.page(1)

    context={'title':'用户中心', 'user_name':user_name,'order':list,'t_pages':total_pages }
    return render(request, "df_user/user_center_order.html", context)

def user_order_handle(request):
    user_name=request.session.get('user_name')
    user_id=request.session.get('user_id')
    index=request.GET['index']
    order=OrderInfo.objects.filter(user=user_id).order_by('-oid')
    #values返回字典的形式
    #order_d=OrderInfo.objects.filter(user=user_id).order_by('-oid').values()
    # print(order[0].odate.strftime("%Y-%m-%d %H:%M:%S"),order_d[0]['odate'])
    Page=Paginator(order,2)
    Page_total=Page.count/2
    if (Page_total - int(index)>-1):
        print('dayu')
        list=Page.page(index)
        glist=[]
        for a in list.object_list:
            #strftime 将datetime(2018, 5, 10, 6, 19, 44, 278277转换成如("%Y-%m-%d %H:%M:%S")'的2018-05-10 06:19:44'
            date=(a.odate).strftime("%Y-%m-%d %H:%M:%S")
            detail=a.orderdetail_set.all()
            dlist=[]

            for d in detail:

                dlist.append({'gtitle':d.goods.gtitle,
                              'gpic':str(d.goods.gpic),
                              'gprice':d.goods.gprice,
                              'count':d.count,
                              'gunit':d.goods.gunit,

                              })
            glist.append({'odate':date, 'ototal':a.ototal, 'oid':a.oid, 'ostatus':a.ostatus,'g_l':dlist})

        return JsonResponse({'status':1, 'js': index, 'goods': glist})
    else:
        print('xiaoyu')
        return JsonResponse({'status':0})
@user_decorator.login
def user_center_site(request):
    user_name=request.session.get('user_name')
    user_info=UserInfo.user2.get(uname=user_name)
    user_shou=user_info.ushou
    user_address=user_info.uaddress
    user_phone=user_info.uphone
    user_youbian=user_info.uyoubian
    context={
        'user_name':user_name, 'user_shou':user_shou, 'user_address':user_address,
        'user_youbian':user_youbian, 'user_phone':user_phone, 'title':'用户中心',
             }
    return render(request, "df_user/user_center_site.html", context)

#处理编辑地址
def user_center_site_handle(request):
    post=request.POST
    user_name=request.session.get('user_name')
    get_shou=post.get('shou')
    get_youbian=post.get('youbian')
    get_iphone=post.get('iphone')
    get_site_area=post.get('site_area')
    user_info=UserInfo.user2.get(uname=user_name)
    user_info.ushou=get_shou
    user_info.uaddress=get_site_area
    user_info.uphone=get_iphone
    user_info.uyoubian=get_youbian
    user_info.save()
    return redirect('/user/user_center_site/')

def exit_use(request):

    request.session.flush()
    return render(request, 'df_user/login.html')

#分别定义404和500页面：
def page_not_found(request):
    return redirect('http://www.baidu.com')
