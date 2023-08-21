from django.db import models
from utility.mixins import UUIDMixin
from usermgmt.models import User

# Create your models here.

PAYMENT_STATUS = (
    ('done','Done'),
    ('pending','Pending'),
    ('cancelled','Cancelled'),
)

class Payment(UUIDMixin):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='user_payment')
    order_id = models.CharField(max_length=50,blank=True)
    payment_status = models.CharField(max_length=20,choices=PAYMENT_STATUS)
    amount = models.IntegerField()
    razorpay_order_id = models.CharField(max_length=50,blank=True)
    razorpay_payment_id = models.CharField(max_length=50,blank=True)

    def __str__(self) -> str:
        return self.user.email