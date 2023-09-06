from django.db import models
from utility.mixins import UUIDMixin
from usermgmt.models import User

# Create your models here.
PAYMENT_STATUS = (
    ('created','Created'),
    ('authorised','Authorised'),
    ('captured','Captured'),
    ('failed','Failed'),
    ('refunded','Refunded'),
)


class Payment(UUIDMixin):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='user_payment')
    order_id = models.CharField(max_length=50,blank=True,db_index=True)
    payment_status = models.CharField(max_length=20,blank=True,choices=PAYMENT_STATUS)
    payment_method = models.CharField(max_length=20,blank=True)
    payment_detail = models.CharField(max_length=20,blank=True)
    amount = models.IntegerField()
    razorpay_order_id = models.CharField(max_length=50,blank=True,db_index=True)
    razorpay_payment_id = models.CharField(max_length=50,blank=True,db_index=True)
    razorpay_signature = models.CharField(max_length=100,blank=True,db_index=True)
    is_payment_status_updated = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.user.email