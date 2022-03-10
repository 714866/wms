from django.conf.urls import url
from . import views
from .views import *
urlpatterns=[
    url(r'^index/', views.index),
    url(r'^detail', views.detail),
    url(r'^list', views.list),
    url(r'^deal_list', views.deal_list),
    url(r'^search/',MySearchView()),
]