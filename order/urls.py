from django.conf.urls import url
from .swagger_view import MqOrder

urlpatterns=[
    url(r'^mqOrdert/', MqOrder.as_view(),name='order'),
    # url(r'^AlbumViewset/', AlbumViewset().as_view(),name='order2'),


]