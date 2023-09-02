from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver
from .models import Product

@receiver(signal=post_save,sender=Product)
def increase_brand_total_products(sender,instance,created,**kwargs):
    brand = instance.brand
    brand.total_products +=1
    brand.save()

@receiver(signal=post_delete,sender=Product)
def decrease_brand_total_products(sender,instance,**kwargs):
    brand = instance.brand
    brand.total_products -=1
    brand.save()
