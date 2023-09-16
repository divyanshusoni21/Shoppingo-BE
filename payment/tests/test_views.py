from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from ..models import *
from usermgmt.models import User

class PaymentTestCase(APITestCase):

    def setUp(self) -> None:
        # create a user
        user = User(email='abc@gmail.com',is_active=True,is_verified=True)
        user.set_password('Admin123@')
        user.save()
        self.user = user
        accessToken = user.tokens()['access']
        self.headers = {'Authorization':f'Bearer {accessToken}'}


    def test_payment_initialize(self):
        url = reverse('payment_initialize')
        data={
                "amount":10
            }
        resposne = self.client.post(url,data, headers=self.headers ,format='json')
        self.assertEqual(resposne.status_code,status.HTTP_200_OK)
        responseData = resposne.data

        self.assertIn("razorpay_order_id",responseData)
        self.assertEqual(responseData["amount"],10)
        self.assertEqual(responseData["payment_status"],PAYMENT_STATUS[0][0])
        self.assertEqual(responseData["razorpay_payment_id"],"")
        self.assertEqual(responseData["razorpay_signature"],"")
        self.assertEqual(responseData["user"],self.user.id)

        # test without giving access token
        resposne = self.client.post(url,data ,format='json')
        self.assertEqual(resposne.status_code,status.HTTP_401_UNAUTHORIZED)

    def test_payment_handler(self):
        payment = Payment.objects.create(
                                        user = self.user,
                                        amount = 10,
                                        razorpay_order_id = 'order_MZ8YrLyLAAA4qO',
                                        payment_status = PAYMENT_STATUS[0][0], # created
                                    )
        
        url = reverse("payment_handler")
        data = {
                "razorpay_order_id":"order_MZ8YrLyLAAA4qO",
                "razorpay_payment_id":"pay_MZ8bXuWrJmLlui",
                "razorpay_signature":"dfeaf5d51c3a286b0189c5e1db621d402b3c1cfea8fd4b8deeef4124f0b41f36"
            }
        response = self.client.post(url,data, headers=self.headers, format='json')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        responseData = response.data
        self.assertEqual(responseData["razorpay_order_id"],"order_MZ8YrLyLAAA4qO")
        self.assertEqual(responseData["razorpay_payment_id"],"pay_MZ8bXuWrJmLlui")
        self.assertEqual(responseData["razorpay_signature"],"dfeaf5d51c3a286b0189c5e1db621d402b3c1cfea8fd4b8deeef4124f0b41f36")
        self.assertEqual(responseData["amount"],10)
        self.assertEqual(responseData["payment_status"],PAYMENT_STATUS[2][0]) # captured

        # test with wrong razorpay order id 
        data["razorpay_order_id"] = "order_MZ8YrAA4qO"
        response = self.client.post(url,data, headers=self.headers, format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        data["razorpay_order_id"] = "order_MZ8YrLyLAAA4qO"

        # test without access token
        response = self.client.post(url,data, format='json')
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)

        # test without giving payment id
        data = {
                "razorpay_order_id":"order_MZ8YrLyLAAA4qO",
                "razorpay_signature":"dfeaf5d51c3a286b0189c5e1db621d402b3c1cfea8fd4b8deeef4124f0b41f36"
            }
        response = self.client.post(url,data, headers=self.headers, format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)