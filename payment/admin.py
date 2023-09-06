from django.contrib import admin
from .models import *

# Register your models here.

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user','order_id','amount','payment_status')
    list_filter = ('payment_status',)
    search_fields = ('id','user__id','user__email','order_id','razorpay_order_id','razorpay_payment_id')
admin.site.register(Payment,PaymentAdmin)