from django.http import JsonResponse
from rest_framework.exceptions import APIException


def Singleton(cls):
    '''单例装饰器'''
    __instance={}
    def _sing_leton(*args,**kwargs):
        if cls not in __instance:
            __instance[cls]=cls(*args,**kwargs)
        return __instance[cls]
    return _sing_leton


def catch_exception(cls):
    '''异常'''
    def get_except(*args,**kwargs):
        try:
            return cls(*args,**kwargs)
        # except Exception as e :
        except APIException as e :
            return JsonResponse({"error_messge":str(e)})
    return get_except