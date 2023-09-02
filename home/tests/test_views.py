from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from ..models import *
from django.core.files.uploadedfile import SimpleUploadedFile
from ..serializers import ProductSerializer
from django.test.client import RequestFactory


class HomeTestCase(APITestCase):

    def setUp(self) -> None:
        self.category = Category.objects.create(category = 'fashion')
        self.subCategory = SubCategory.objects.create(category = self.category , sub_category= "Men's tshirt")
        brand = Brand.objects.create(brand_name = 'Ajio')
        tag = ProductTag.objects.create(tag = 'Fashion')
        image = SimpleUploadedFile("test_image.jpg", content=b"image_data", content_type="image/jpeg")
        
        product = Product.objects.create(
                name = 'test product',
                description= 'lorem ipsum',
                price = 100 ,
                image = image,
                category = self.subCategory,
                brand = brand,
            )
        product.tags.add(tag)
        self.prodcut = product

    def test_get_product_details(self):
        url = reverse('product',kwargs={'productId':self.prodcut.id})

        response = self.client.get(url,format='json')
        self.assertEqual(response.status_code , status.HTTP_200_OK)

        data = response.json()
        self.assertIn('image',data)
        self.assertIn('brand_name',data['brand'])
        self.assertIn('sub_category',data['category'])
        self.assertIn('tag',data['tags'][0])
        
        self.assertEqual(data['name'],self.prodcut.name)
        self.assertEqual(data['brand']['brand_name'],self.prodcut.brand.brand_name)
        self.assertEqual(data['category']['sub_category'],self.prodcut.category.sub_category)

        # test with wrong product id
        url = reverse('product',kwargs={'productId':self.category.id})
        response = self.client.get(url,format='json')
        self.assertEqual(response.status_code , status.HTTP_400_BAD_REQUEST)

    def test_get_categories(self):
        ''' test '''
        url = reverse('category-list')
        
        response = self.client.get(url,format='json')
        self.assertEqual(response.status_code,status.HTTP_200_OK)

        data = response.json()

        self.assertIn('category',data[0])
        self.assertIn('sub_category',data[0]['sub_categories'][0])

        self.assertEqual(data[0]['category'],self.category.category)
        self.assertEqual(data[0]['sub_categories'][0]['sub_category'],self.subCategory.sub_category)
    
    def test_get_products_by_category(self):
        url = reverse('category-detail',args=[self.subCategory.id])
        response = self.client.get(url,format='json')
        self.assertEqual(response.status_code,status.HTTP_200_OK)

        data = response.json()
        
        # Create a RequestFactory instance to replicate request to pass in serializer
        factory = RequestFactory()
        # Create a GET request and attach the user to it
        request = factory.get(url)

        productData = ProductSerializer(self.prodcut,context={'request':request}).data
        self.assertEqual(productData,data[0]) 

        # test with a wrong sub category id 
        url = reverse('category-detail',args=[self.category.id])
        response = self.client.get(url,format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)