from django.conf.urls import url
# from . import views
from .views import *
from django.urls import path


urlpatterns=[
    url(r'^login/', PdaLogin.as_view(),name='手持登录接口'),
    url(r'^createtwmspck/', TwmsOdsPckInfo.as_view(),name='twms新增接口'),


]