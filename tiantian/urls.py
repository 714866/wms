#encoding=utf-8
"""tiantian URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url('admin/',admin.site.urls),
    # url(r'^user/', include('df_user.urls')),
    # url(r'^goods/', include('df_goods.urls')),
    # url(r'^cart/', include('cart.urls')),
    # url(r'^order/',include('order.urls')),
    url('DBcreateOrder/',include('DBcreateOrder.urls')),
    # url(r'^search/', include('haystack.urls')),
]

#配置404和500返回页面
from django.conf.urls import handler404, handler500


# handler404 = "DBcreateOrder.views.page_error"
#（handler404 = "你的app.views.函数名"）
# handler500 = "df_user.views.page_error"