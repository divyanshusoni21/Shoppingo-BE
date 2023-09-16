from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from ..models import *
from home.models import Product,Brand,Category,SubCategory,ProductTag
from payment.models import Payment


class OrderTestCase(APITestCase):
        
    def setUp(self) -> None:
        # creating product ,user and payment object to use in all test cases
        
        # create a product
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
        
        # create a user
        user = User(email='abc@gmail.com',is_active=True,is_verified=True)
        user.set_password('Admin123@')
        user.save()
        self.user = user
        accessToken = user.tokens()['access']
        self.headers = {'Authorization':f'Bearer {accessToken}'}

        # create a payment
        payment = Payment.objects.create(user = user , amount = 100)
        self.payment = payment

    def test_create_order(self):
        url = reverse('order-list')

        data = {
            "payment_id" : self.payment.id,
            "order_location":"lorem ipsum",
            "total_item":2,
            "paid_amount":200,
            "items":[
                {
                    "product":self.product.id,
                    "quantity":2
                }
            ]
        }

        resposne = self.client.post(url,data,headers = self.headers,format='json')
        self.assertEqual(resposne.status_code,status.HTTP_200_OK)

        responseData = resposne.json()

        # check response format
        self.assertIn('id',responseData)
        self.assertIn("order_items",responseData)
        self.assertIn("product",responseData["order_items"][0])

        self.assertEqual(responseData["order_status"],ORDER_STATUS[0][0]) # booked
        self.assertEqual(responseData["order_items"][0]["product"],str(self.product.id))

        # test creating order with same payment id
        resposne = self.client.post(url,data,headers = self.headers,format='json')
        self.assertEqual(resposne.status_code,status.HTTP_400_BAD_REQUEST)

        # test giving wrong payment id
        data['payment_id'] = self.user.id
        resposne = self.client.post(url,data,headers = self.headers,format='json')
        self.assertEqual(resposne.status_code,status.HTTP_400_BAD_REQUEST)
        data['payment_id'] = self.payment.id

        # test giving wrong product id
        data["items"][0]["product"] = self.user.id
        resposne = self.client.post(url,data,headers = self.headers,format='json')
        self.assertEqual(resposne.status_code,status.HTTP_400_BAD_REQUEST)
        data["items"][0]["product"] = self.product.id

        # test hitting api without access token
        resposne = self.client.post(url,data,format='json')
        self.assertEqual(resposne.status_code,status.HTTP_401_UNAUTHORIZED)
    
    def test_get_user_orders(self):
        # create a order
        url = reverse('order-list')

        data = {
            "payment_id" : self.payment.id,
            "order_location":"lorem ipsum",
            "total_item":2,
            "paid_amount":200,
            "items":[
                {
                    "product":self.product.id,
                    "quantity":2
                }
            ]
        }

        resposne = self.client.post(url,data,headers = self.headers,format='json')
        self.assertEqual(resposne.status_code,status.HTTP_200_OK)

        # testing get user's order api
        url = reverse('order-list')

        response = self.client.get(url,headers=self.headers)
        self.assertEqual(response.status_code,status.HTTP_200_OK)

        responseData = response.data
        
        # check response format

        # >>> pagination response >>>
        self.assertIn("count",responseData)
        self.assertIn("next",responseData)
        self.assertIn("previous",responseData)
        self.assertIn("results",responseData)

        self.assertIn('id',responseData["results"][0])
        self.assertIn("order_items",responseData["results"][0])
        self.assertIn("product",responseData["results"][0]["order_items"][0])

        self.assertEqual(responseData["results"][0]["order_status"],ORDER_STATUS[0][0]) # booked
        self.assertEqual(responseData["results"][0]["order_items"][0]["product"]["id"],str(self.product.id))

        # test hitting api without access token
        resposne = self.client.get(url)
        self.assertEqual(resposne.status_code,status.HTTP_401_UNAUTHORIZED)

    def test_get_order_details(self):
        # create a order
        url = reverse('order-list')

        data = {
            "payment_id" : self.payment.id,
            "order_location":"lorem ipsum",
            "total_item":2,
            "paid_amount":200,
            "items":[
                {
                    "product":self.product.id,
                    "quantity":2
                }
            ]
        }

        resposne = self.client.post(url,data,headers = self.headers,format='json')
        self.assertEqual(resposne.status_code,status.HTTP_200_OK)

        orderId = resposne.data['order_id']
        url = reverse('order-detail',args=(orderId,))
        response = self.client.get(url,headers=self.headers)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        responseData = response.json()
        
        # check response format
        self.assertIn('id',responseData)
        self.assertIn("order_items",responseData)
        self.assertIn("product",responseData["order_items"][0])

        self.assertEqual(responseData["order_status"],ORDER_STATUS[0][0]) # booked
        self.assertEqual(responseData["order_items"][0]["product"]["id"],str(self.product.id))

        # test without giving access token
        response = self.client.get(url)
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)

        # test with wrong order id
        url = reverse('order-detail',args=('dfksdfkah',))
        response = self.client.get(url,headers=self.headers)
       
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)

    def test_update_order_status_lifecycle_signal(self):
        # create a order
        url = reverse('order-list')

        data = {
            "payment_id" : self.payment.id,
            "order_location":"lorem ipsum",
            "total_item":2,
            "paid_amount":200,
            "items":[
                {
                    "product":self.product.id,
                    "quantity":2
                }
            ]
        }

        resposne = self.client.post(url,data,headers = self.headers,format='json')
        self.assertEqual(resposne.status_code,status.HTTP_200_OK)
        responseData = resposne.data
        self.assertIn(ORDER_STATUS[0][0],responseData['order_lifecycle']) # booked
        self.assertNotIn(ORDER_STATUS[1][0],responseData['order_lifecycle']) # shipped

        # after updating order status , order lifecycle should also be updated
        orderId = responseData["order_id"]
        order = Order.objects.get(order_id = orderId)
        order.order_status = ORDER_STATUS[1][0] #shipped
        order.save()
        self.assertIn(ORDER_STATUS[1][0],order.order_lifecycle) # shipped
        self.assertNotIn(ORDER_STATUS[2][0],order.order_lifecycle) # delivered

        order.order_status = ORDER_STATUS[2][0] # delivered
        order.save()
        self.assertIn(ORDER_STATUS[2][0],order.order_lifecycle) # delivered



    