from django.test import TestCase
from ..models import Product,Brand,Category,SubCategory,ProductTag
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils.text import slugify

class HomeModeltestCase(TestCase):

    def test_slug_created(self):
                # creating product and user to use in all test cases
        productName = 'test product'
        self.category = Category.objects.create(category = 'fashion')
        self.subCategory = SubCategory.objects.create(category = self.category , sub_category= "Men's tshirt")
        brand = Brand.objects.create(brand_name = 'Ajio')
        tag = ProductTag.objects.create(tag = 'Fashion')
        image = SimpleUploadedFile("test_image.jpg", content=b"image_data", content_type="image/jpeg")
        
        product = Product.objects.create(
                name = productName,
                description= 'lorem ipsum',
                price = 100 ,
                image = image,
                category = self.subCategory,
                brand = brand,
            )
        product.tags.add(tag)

        self.assertEqual(product.slug , slugify(productName))