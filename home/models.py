from django.db import models
from utility.mixins import UUIDMixin
from usermgmt.models import User
from django.utils.text import slugify


# Create your models here.

class Category(UUIDMixin):
    category = models.CharField(max_length=50)
    
    def __str__(self) -> str:
        return self.category

class SubCategory(UUIDMixin):
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    sub_category = models.CharField(max_length=50,db_index=True)

    def __str__(self) -> str:
        return self.sub_category
    
class ProductTag(UUIDMixin):
    tag = models.CharField(max_length=50)
    
    def __str__(self) -> str:
        return self.tag
    
class Brand(UUIDMixin):
    brand_name = models.CharField(max_length=50,db_index=True)
    total_products = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.brand_name

class Product(UUIDMixin):
    name = models.CharField(max_length=255,db_index=True)
    description = models.TextField(blank=True)
    price = models.IntegerField()
    image = models.ImageField(upload_to="product/image")
    category = models.ForeignKey(SubCategory, on_delete=models.CASCADE, null=True)
    tags = models.ManyToManyField(ProductTag)
    rating = models.DecimalField(decimal_places=1, max_digits=3, default=0.0)
    discount = models.IntegerField(default=0)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    benefits = models.TextField(blank=True)
    how_to_use = models.TextField(blank=True)
    sold_units = models.IntegerField(default=0)
    ingredients = models.TextField(blank=True)
    slug = models.SlugField(db_index=True,blank=True)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)

class ProductReview(UUIDMixin):
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='product_review')
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='user_product_review')
    review = models.TextField(blank=True)
    rating = models.DecimalField(decimal_places=1, max_digits=3, default=0.0)

    def __str__(self) -> str:
        return self.product.name


class UserCart(UUIDMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    
    def __str__(self):
        
        return self.user.email + f" ({self.product.name})"
    
class Inventory(UUIDMixin):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return self.product.name
