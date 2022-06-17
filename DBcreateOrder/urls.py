from django.conf.urls import url
from . import views
from .views import *


urlpatterns=[
    url(r'^index/', views.index),
    url(r'^returnResult/', views.returnResult),
    url(r'^InStorageRequest', views.InStorageRequest),
    url(r'^virtualInStorageRequest', views.virtualInStorageRequest)
]