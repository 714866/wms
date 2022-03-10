from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^register/$', views.register),
    url(r'^register_exit/$', views.register_exit),
    url(r'^register_handle/$', views.register_handle),
    url(r'^login/$', views.login),
    url(r'^login_handle/$', views.login_handl),
    url(r'^user_center_info/$', views.user_center_info),
    url(r'^user_center_order/$', views.user_center_order),
    url(r'^user_center_site/$', views.user_center_site),
    url(r'user_center_site_handle/$', views.user_center_site_handle),
    url(r'exit_use/$', views.exit_use),
    url(r'user_order_headle/',views.user_order_handle)

]