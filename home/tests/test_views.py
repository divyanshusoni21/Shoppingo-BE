from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from ..models import *
from usermgmt.models import User
from order.models import Order,OrderItem,ORDER_STATUS
from django.core.files.uploadedfile import SimpleUploadedFile
from ..serializers import ProductSerializer
from django.test.client import RequestFactory
from datetime import datetime,timedelta
from utility.variables import expecteddeliveryDays




class HomeTestCase(APITestCase):

    def setUp(self) -> None:
        # creating product and user to use in all test cases
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
        self.product = product

        user = User(email='abc@gmail.com',is_active=True,is_verified=True)
        user.set_password('Admin123@')
        user.save()
        self.user = user
        accessToken = user.tokens()['access']
        self.headers = {'Authorization':f'Bearer {accessToken}'}


    # >>>>>>>>>>>>>>>>>>>> Product apis tests >>>>>>>>>>>>>>>>>>
    def test_get_product_details(self):
        ''' test getting a product details by it's id.'''
        url = reverse('product',kwargs={'productId':self.product.id})

        response = self.client.get(url,format='json')
        self.assertEqual(response.status_code , status.HTTP_200_OK)

        data = response.json()
        # testing the format of response
        self.assertIn('image',data)
        self.assertIn('brand_name',data['brand'])
        self.assertIn('sub_category',data['category'])
        self.assertIn('tag',data['tags'][0])
        
        self.assertEqual(data['name'],self.product.name)
        self.assertEqual(data['brand']['brand_name'],self.product.brand.brand_name)
        self.assertEqual(data['category']['sub_category'],self.product.category.sub_category)

        # test with wrong product id
        url = reverse('product',kwargs={'productId':self.category.id})
        response = self.client.get(url,format='json')
        self.assertEqual(response.status_code , status.HTTP_400_BAD_REQUEST)
    
    # >>>>>>>>>>>>>>>>>>>> Category apis tests >>>>>>>>>>>>>>>>>>
    def test_get_categories(self):
        ''' test getting all categories. '''

        url = reverse('category-list')
        
        response = self.client.get(url,format='json')
        self.assertEqual(response.status_code,status.HTTP_200_OK)

        data = response.json()

        # testing the format of response
        self.assertIn('category',data[0])
        self.assertIn('sub_category',data[0]['sub_categories'][0])

        self.assertEqual(data[0]['category'],self.category.category)
        self.assertEqual(data[0]['sub_categories'][0]['sub_category'],self.subCategory.sub_category)
    
    def test_get_products_by_category(self):
        ''' test getting all product by category id'''
        url = reverse('category-detail',args=[self.subCategory.id])
        response = self.client.get(url,format='json')
        self.assertEqual(response.status_code,status.HTTP_200_OK)

        data = response.json()
        
        # Create a RequestFactory instance to replicate request to pass in serializer
        factory = RequestFactory()
        # Create a GET request and attach the user to it
        request = factory.get(url)

        # test that the product data we get in response is in the required format or not
        productData = ProductSerializer(self.product,context={'request':request}).data
        self.assertEqual(productData,data[0]) 

        # test with a wrong sub category id 
        url = reverse('category-detail',args=[self.category.id])
        response = self.client.get(url,format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
    
    # >>>>>>>>>>>>>>>>>>>> Cart apis tests >>>>>>>>>>>>>>>>>>
    def test_create_cart(self):
        ''' add items to cart '''
        url = reverse('cart-list')
        
        data = {
            "product":self.product.id,
            "quantity":2
        }

        response = self.client.post(url,data,headers=self.headers,format='json')
        self.assertEqual(response.status_code , status.HTTP_200_OK)

        response = self.client.post(url,data,format='json')
        self.assertEqual(response.status_code , status.HTTP_401_UNAUTHORIZED)

        # test with a product id given
        data = {
            "product":self.user.id,
            "quantity":2
        }
        response = self.client.post(url,data,headers=self.headers,format='json')
        self.assertEqual(response.status_code , status.HTTP_400_BAD_REQUEST)
    
    def test_get_cart(self):
        ''' Get items in cart'''
        # create a cart item
        url = reverse('cart-list')
        
        data = {
            "product":self.product.id,
            "quantity":2
        }

        response = self.client.post(url,data,headers=self.headers,format='json')
        self.assertEqual(response.status_code , status.HTTP_200_OK)
        
        # test the get response exact data provided in create
        url = reverse('cart-list')
        response = self.client.get(url,headers=self.headers,format='json')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        
        data = response.json()

        # testing the format of response
        self.assertIn('id',data[0])
        self.assertIn('name',data[0]['product'])

        self.assertEqual(data[0]['product']['id'],str(self.product.id))
        self.assertEqual(data[0]['quantity'],2)

        # test without giving the access token
        response = self.client.get(url,format='json')
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)
    
    def test_update_cart(self):
        # create a cart item
        url = reverse('cart-list')
        
        data = {
            "product":self.product.id,
            "quantity":2
        }

        response = self.client.post(url,data,headers=self.headers,format='json')
        self.assertEqual(response.status_code , status.HTTP_200_OK)
        # update the cart item's quantity
        url = reverse('cart-detail',args=[self.product.id])
        data = {'quantity':3}
        
        response = self.client.patch(url,data,headers=self.headers,format='json')
        self.assertEqual(response.status_code , status.HTTP_200_OK)
        
        # check in get request if quantity was updated
        url = reverse('cart-list')
        response = self.client.get(url,headers=self.headers,format='json')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data[0]['quantity'],3)

        # test without giving the access token
        url = reverse('cart-detail',args=[self.product.id])
        data = {'quantity':3}
        response = self.client.patch(url,data,format='json')
        self.assertEqual(response.status_code , status.HTTP_401_UNAUTHORIZED)
        
        # test with wrong product id
        url = reverse('cart-detail',args=[self.user.id])
        response = self.client.patch(url,data,headers=self.headers,format='json')
        self.assertEqual(response.status_code , status.HTTP_400_BAD_REQUEST)
    
    def test_delete_cart(self):
        # create a cart item
        url = reverse('cart-list')
        
        data = {
            "product":self.product.id,
            "quantity":2
        }

        response = self.client.post(url,data,headers=self.headers,format='json')
        self.assertEqual(response.status_code , status.HTTP_200_OK)
        
        # test delete the created cart item
        url = reverse('cart-detail',args=[self.product.id])
        response = self.client.delete(url,headers=self.headers,format='json')
        self.assertEqual(response.status_code , status.HTTP_200_OK)
        
        # test that get response is empty
        url = reverse('cart-list')
        response = self.client.get(url,headers=self.headers,format='json')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data,[])

        # test without giving the access token
        url = reverse('cart-detail',args=[self.product.id])
        response = self.client.delete(url,data,format='json')
        self.assertEqual(response.status_code , status.HTTP_401_UNAUTHORIZED)
        
        # test with wrong product id
        url = reverse('cart-detail',args=[self.user.id])
        response = self.client.delete(url,data,headers=self.headers,format='json')
        self.assertEqual(response.status_code , status.HTTP_400_BAD_REQUEST)
    
    # >>>>>>>>>>>>>>>>>>>> Product review apis tests >>>>>>>>>>>>>>>>>>
    def test_create_product_review(self):
        url = reverse('product_review')
        data = {
            "product":self.product.id,
            "review":"lorem ipsum",
            "rating":3
        }
        response  = self.client.post(url,data, headers=self.headers , format='json')
        # user would not be able to review the product cause he has not purchased it yet !
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)

        # create a order with status as 'deleivered' of user with product
        orderId = 'test123'
        today = datetime.now()
        expectedDelivery = today+timedelta(days=expecteddeliveryDays)
        order = Order.objects.create(user = self.user , order_id = orderId , order_status = ORDER_STATUS[2][0],
                                     order_date = today,paid_amount=100,expected_delivery = expectedDelivery
                                     )
        OrderItem.objects.create(order=order,product=self.product,quantity = 1)

        # now user should be able to create a product review
        response  = self.client.post(url,data, headers=self.headers , format='json')
        
        self.assertEqual(response.status_code,status.HTTP_200_OK)

        # test without giving access token
        response  = self.client.post(url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)

        # test with a product id
        data = {
            "product":self.user.id,
            "review":"lorem ipsum",
            "rating":3
        }
        response  = self.client.post(url,data, headers=self.headers , format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)