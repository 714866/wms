
from modular.GetApplication import get_value
from django.conf import settings

# configparser模块的配置文件，然后自己写的获取方法
def wsp_url():
    return get_value('wsp_url','url')
def wsp_key():
    return get_value('wsp_url','key')
#直接使用django的配置文件写
def wms_url():
    return settings.WMS_URL

def wms_key():
    return settings.WMS_KEY