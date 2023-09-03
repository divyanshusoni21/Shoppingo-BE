from django.contrib import admin
from .models import *

# Register your models here.

class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id','user','order_status','paid_amount','order_date')
    list_filter = ('order_status',)
    search_fields = ('id','order_id','user__id','user__email','payment_id__id')
admin.site.register(Order,OrderAdmin)

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order','product','quantity')
    search_fields = ('id','order__order_id','product__id','product__name')
admin.site.register(OrderItem,OrderItemAdmin)