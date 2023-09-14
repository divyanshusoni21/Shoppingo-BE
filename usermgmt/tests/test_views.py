from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from ..models import User
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import  smart_bytes

# Create your tests here.
class UsermgmtTestCase(APITestCase):

    def setUp(self) -> None:
        self.email = 'admin@gmail.com'
        self.password = 'Admin231@'

        user = User(email=self.email,username='aman soni',is_active=True,is_verified=True)
        user.set_password(self.password)
        user.save()
        self.user = user

        self.uidb64 = urlsafe_base64_encode(smart_bytes(self.user.id))


    def test_create_user(self):
        url=reverse('register')
        data = {
            'username':'aman soni',
            'email':'admin@gmail.com',
            'password':'Admin321@'
        }
        response = self.client.post(url,data,format='json')
       
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        self.assertIn('error',response.json())
        
        data = {
            'username':'aman soni',
            'email':'aman@gmail.com',
            'password':'aDmin421@'
        }
        response = self.client.post(url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        self.assertIn('success',response.json())


    def test_verify_email(self):
        
        url = reverse('verify_email')
        data = {'code':self.uidb64}
        response = self.client.post(url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        

        self.assertIn('access',response.json())
        self.assertIn('refresh',response.json())
        self.assertIn('username',response.json())

        self.assertIsInstance(response.json()['access'],str)
        self.assertIsInstance(response.json()['refresh'],str)
        self.assertIsInstance(response.json()['username'],str)

        uidb64 = 'sdaiebdweg23c7bcvd'
        data = {'code':uidb64}
        response = self.client.post(url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)

                               
    def test_login(self):
        url = reverse('login')
        data={'email':self.email,'password':self.password}
        response = self.client.post(url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
    

        self.assertIn('access',response.json())
        self.assertIn('refresh',response.json())
        self.assertIn('username',response.json())

        self.assertIsInstance(response.json()['access'],str)
        self.assertIsInstance(response.json()['refresh'],str)
        self.assertIsInstance(response.json()['username'],str)

        data={'email':self.email,'password':'admin231'}
        response = self.client.post(url,data,format='json')
        self.assertNotEqual(response.status_code,status.HTTP_200_OK)


    def test_forget_password(self):
        url = reverse('forget_password',kwargs={'email':self.email})
        response = self.client.get(url,format='json')
        self.assertEqual(response.status_code , status.HTTP_200_OK)

        url = reverse('forget_password',kwargs={'email': 'divyanshusoni@gmail.com'})
        response = self.client.get(url,format='json')
        self.assertEqual(response.status_code , status.HTTP_400_BAD_REQUEST)

    
    def test_reset_password(self):
        url = reverse('reset_password')
        newPassword = 'Divyanhsu301'
        body = {
            'code':self.uidb64,
            'password':newPassword
        }
        response = self.client.post(url,body,format = 'json')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertIsInstance(response.json()['access'],str)
        self.assertIsInstance(response.json()['refresh'],str)
        self.assertIsInstance(response.json()['username'],str)

        loginUrl = reverse('login')
        data={'email':self.email,'password':self.password}
        response = self.client.post(loginUrl,data,format='json')

        data={'email':self.email,'password':newPassword}
        response = self.client.post(loginUrl,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_200_OK)

        uidb64 = 'sdaiebdweg23c7bcvd'
        body = {
            'code':uidb64,
            'password':newPassword
        }
        response = self.client.post(url,body,format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)


        
