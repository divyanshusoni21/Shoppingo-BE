from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import  smart_bytes
from usermgmt.models import User
user = User.objects.filter(email='test@gmail.com')
uidb = urlsafe_base64_encode(smart_bytes(user[0].id))
print(f'uidb ; {uidb}')