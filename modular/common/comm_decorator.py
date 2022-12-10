def Singleton(cls):
    '''单例装饰器'''
    __instance={}
    def _sing_leton(*args,**kwargs):
        if cls not in __instance:
            __instance[cls]=cls(*args,**kwargs)
        return __instance[cls]
    return _sing_leton
