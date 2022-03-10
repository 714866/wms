from django.contrib import admin
from .models import *

class TypeInfoAdmin(admin.ModelAdmin):
    list_display = ['id','ttitle']

# class GoodInfoAdmin(admin.ModelAdmin):
#     list_per_page = 15
#     list_display = ['id','ttitle']


admin.site.register(TypeInfo,TypeInfoAdmin)
admin.site.register(GoodsInfo)

