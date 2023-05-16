from django.conf.urls import url
# from . import views
from .views import *
from django.urls import path


urlpatterns=[
    url(r'^login/', PdaLogin.as_view(),name='手持登录接口'),
    url(r'^createtwmspck/', TwmsOdsPckInfo.as_view(),name='twms新增接口'),
    url(r'^saveShelf/', PdaSaveShelf.as_view(),name='入库签收接口'),
    url(r'^saveReceipt/', PdaSaveReceipt.as_view(),name='收货接口'),
    url(r'^saveInstorage/', PdaSaveInStorage.as_view(),name='入库接口'),
    url(r'^UpdateShelfRack/', PdaUpdateShelfRack.as_view(),name='上架接口'),
    url(r'^goodsShelf/', goodsShelf.as_view(),name='从SFT生成到上架'),
    url(r'^AllocationTask/', AllocationTask.as_view(),name='纸质配货'),


]