from django.db import models
from home.models import Product
from usermgmt.models import User
from utility.mixins import UUIDMixin
from payment.models import Payment

# Create your models here.

ORDER_STATUS = (
    ('booked','Booked'),
    ('shipped','Shipped'),
    ('delivered','Delivered'),
    ('cancelled','Cancelled'),
)

class Order(UUIDMixin):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='user_order')
    order_date = models.DateTimeField()
    order_lifecycle = models.JSONField(default=dict,null=True,blank=True)
    order_status = models.CharField(choices=ORDER_STATUS,max_length=20,default=ORDER_STATUS[0][0])
    order_id = models.CharField(max_length=50, blank=True, db_index=True)
    order_location = models.TextField(blank=True)
    total_item = models.IntegerField(default=1)
    paid_amount = models.CharField(max_length=50)
    payment_id = models.OneToOneField(Payment, on_delete=models.CASCADE, null=True, blank=True,related_name='payment_order')
    expected_delivery = models.DateField()

    def __str__(self) -> str:
        return self.user.email
    

class OrderItem(UUIDMixin):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return self.order.user.email + f" ({self.product.name})"
    