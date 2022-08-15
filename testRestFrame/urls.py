from django.contrib import admin
from rest_framework import routers
from django.conf.urls import url, include

# 下面是刚才自定义的schema
from testRestFrame.schema_view import SwaggerSchemaView
# 自定义接口
from testRestFrame.tests import CustomView
from testRestFrame.views import CustomView1

router = routers.DefaultRouter()

urlpatterns = [
    # swagger接口文档路由
    url(r"^docs/$", SwaggerSchemaView.as_view()),
    # url(r'^admin/', admin.site.urls),
    # url(r'^', include(router.urls)),
    # drf登录
    # url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # 测试接口
    url(r'^test1/$', CustomView.as_view(), name='test1'),
    url(r'^test2/$', CustomView1.as_view(), name='test2'),
]