
from django.test import TestCase
from ..models import User


class UserModelTestCase(TestCase):

    def test_create_user(self):
        username = 'aman soni'
        email = 'aman@gmail.com'
        password = 'aman431'
        user = User(email=email,username=username)
        user.set_password(password)
        user.save()

        self.assertEqual(user.email,email)
        self.assertTrue(user.check_password(password))
        self.assertFalse(user.is_active)
        self.assertFalse(user.is_verified)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):

        email = 'aman@gmail.com'
        password = 'aman431'

        superuser = User.objects.create_superuser(email = email , password=password)

        self.assertEqual(superuser.email,email)
        self.assertTrue(superuser.check_password(password))
        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_active)
        self.assertFalse(superuser.is_verified)