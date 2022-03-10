from django.conf.urls import url
from . import views
urlpatterns=[
    url('order_index/$',views.order_index),
    url('deal/$',views.order_deal),
]