from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Order
from datetime import datetime

@receiver(pre_save, sender=Order)
def update_order_status_lifecycle(sender, instance,**kwargs):
    
    today = datetime.now()
    orderStatus = instance.order_status
    lifecycle = instance.order_lifecycle
    lifecycle[orderStatus] = str(today)
    instance.order_lifecycle = lifecycle