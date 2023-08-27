import os
import random
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import  smart_bytes
from django.urls import reverse
from email_func.email import Email
from .variables import emailVerificationPath,resetPasswordEmailPath
from shoppingo.settings import FE_DOMAIN

def generate_verification_link(user,linkType='register'):
    uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
    path = ''
    if linkType == 'register':
        path = emailVerificationPath
    elif linkType == 'forget-password':
        path = resetPasswordEmailPath
        
    customUrl = FE_DOMAIN + path +"?uidb="+str(uidb64)
    return customUrl

def runSerializer(serializerClass,data,partial=False,obj = None) -> tuple :
    ''' creates or updates model object with serializer class , returns object and data as tuple'''
    if partial == True :
        serializer = serializerClass(obj , data=data , partial = partial)
    else :
        serializer = serializerClass(data=data)
    
    serializer.is_valid(raise_exception=True)
    obj = serializer.save()
    return (obj,serializer)

def createDirectory(path):
    os.makedirs(path)

def create_slug(modelClass,lookUpField = 'slug'):
    
    ''' get a model class and lookup field and create a slug for it's new object'''
    # default lookup field will be 'slug' 
    modelName = modelClass.__name__ # get the model class name
    
    slug = modelName +'_'
    
    while True :
        slug+= str(random.randint(100000,1000000))
        # creating a dynamic arguments
        kwargs = {f'{lookUpField}':slug}
        
        if not modelClass.objects.filter(**kwargs):
            break
    return slug

def check_directory_exists(path):
    return os.path.exists(path)

def sendMail(body,email,subject):
    data = {'email_body': body, 
            'to_email': email,
            'email_subject': subject
            }
            
    Email.send_email(data)


def send_token_response(user):
    data = {
        "refresh": str(user.tokens()["refresh"]),
        "access": str(user.tokens()["access"]),
        "username": user.username,

    }
    return data