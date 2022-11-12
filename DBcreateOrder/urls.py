from django.conf.urls import url
from . import views
from .swagger_view import CreatePSRCommon
from .views import *
from django.urls import path


urlpatterns=[
    url(r'^index/', views.index),
    url(r'^returnResult/', views.returnResult),
    url(r'^InStorageRequest$', views.InStorageRequest),
    url(r'^virtualInStorageRequest', views.virtualInStorageRequest),
    url(r'^InStorageRequestPPL$', views.InStorageRequestPPL),
    url(r'^virtualInstorageRequestPPL$', views.virtualInstorageRequestPPL),
    url(r'^getPsr$', views.getPsr),
    url(r'^virtualSyncSFT$', views.virtualSyncSFT),
    url(r'^thirdPsr$', views.thirdPsr),
    url(r'^testPsr$', CreatePSRCommon.as_view(), name='test3'),

]