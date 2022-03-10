from django.conf.urls import url
from . import views
urlpatterns=[
    url(r'cart/$',views.Cart),
    url(r'cart_handle/',views.Cart_handle),
    url(r'cart_delete_(\d*)/$',views.Cart_delete),
    url(r'cart_count/$',views.Cart_number),
    # url(r'order/$',views.Cart_gg),
]