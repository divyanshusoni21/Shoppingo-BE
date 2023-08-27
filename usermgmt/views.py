from .models import User
from .serializers import UserSerializer

from shoppingo.settings import logger
from utility.global_functions import generate_verification_link,sendMail,send_token_response,runSerializer
import traceback

from rest_framework.response import Response
from rest_framework import status,generics,viewsets,permissions
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import smart_str
from datetime import datetime


class RegisterViewSet(generics.GenericAPIView):

    permission_classes = (permissions.AllowAny,)
    serializer_class = UserSerializer

    def post(self,request):
        try :
            # check if email already exists 
            email = request.data['email']
            if User.objects.filter(email=email):
                logger.warning(f'errror : An user already exists with this email !')
                return Response({'error':"An user already exists with this email !"},status=status.HTTP_400_BAD_REQUEST)

            # create user      
            user = runSerializer(self.serializer_class,request.data)[0]
            
            # send email with verification link to verify email
            verificationUrl = generate_verification_link(user)

            email_body = {  
                            "username":user.username,
                            'link':verificationUrl,
                            'type':'registration'           
                        }
            sendMail(email_body,user.email,subject='Verify your email')

            return Response({'success':'An email has been to verify email !'}, status=status.HTTP_201_CREATED)
        except Exception as e :
            logger.warning(traceback.format_exc())
            return Response({'error':str(e)},status=status.HTTP_400_BAD_REQUEST)

class VerifyEmailViewSet(generics.GenericAPIView):
    permission_classes = []

    def post(self,request):
        try :
            code = request.data['code']
            # get user with uidb64 code
            smartId = smart_str(urlsafe_base64_decode(code))
            user = User.objects.filter(id=smartId)
            
            if not user :
                logger.warning(f'error : Invalid code')
                return Response({'error':'Invalid code'},status=status.HTTP_400_BAD_REQUEST)  
            
            user = user[0]
            user.is_active = True
            user.is_verified = True
            user.last_login = datetime.now()  # record last login time
            user.save()

            # generate tokens for user
            data = send_token_response(user)
            return Response(data,status=status.HTTP_200_OK)

        except Exception as e :
            logger.warning(traceback.format_exc())
            return Response({'error':str(e)},status=status.HTTP_400_BAD_REQUEST)

class LoginViewSet(generics.GenericAPIView):
    permission_classes = []
    
    def post(self,request):
        try :
            email = request.data['email']
            password = request.data['password']

            user = User.objects.filter(email = email)
            if user :
                user = user[0]
                if user.check_password(password):

                    if not user.is_active :
                        logger.warning(f'error : Account is inactive')
                        return Response({'error':'Account is inactive'},status=status.HTTP_400_BAD_REQUEST)
                    if not user.is_verified :
                        logger.warning(f'error : Account is not verified')
                        return Response({'error':'Account is not verified'},status=status.HTTP_400_BAD_REQUEST)
                    
                    # record last login time
                    user.last_login = datetime.now()
                    user.save()

                    # generate tokens for user
                    data = send_token_response(user)
                    return Response(data,status=status.HTTP_200_OK)
            
            logger.warning('error : Invalid Credientials !')
            return Response({'error':'Invalid Credientials !'},status=status.HTTP_400_BAD_REQUEST)

        except Exception as e :
            logger.warning(traceback.format_exc())
            return Response({'error':str(e)},status=status.HTTP_400_BAD_REQUEST)            

class ForgetPasswordViewSet(generics.GenericAPIView):
    permission_classes = []

    def get(self,request,email):
        try :
            user = User.objects.filter(email = email,is_active=True)
            if user.exists() :
                user = user[0]
                # send email with verification link
                verificationUrl = generate_verification_link(user,'forget-password')
                email_body = {  
                                "username":user.username,
                                'link':verificationUrl,
                                'type':'forget-password'           
                            }
                sendMail(email_body,email,subject='Reset Password')
                return Response({'success':"An email has been sent to reset your password."},status=status.HTTP_200_OK)
            
            logger.warning(f'error : No user found with this email!')
            return Response({'error':'No user found with this email!'},status=status.HTTP_400_BAD_REQUEST)  

        except Exception as e :
            logger.warning(traceback.format_exc())
            return Response({'error':str(e)},status=status.HTTP_400_BAD_REQUEST)

class ResetPasswordViewSet(generics.GenericAPIView):
    permission_classes = []

    def post(self,request):
        try :
            code = request.data['code']
            password = request.data['password']
            # get user with uidb64 code
            smartId = smart_str(urlsafe_base64_decode(code))
            user = User.objects.filter(id=smartId)
            
            if not user :
                logger.warning(f'error : Invalid code')
                return Response({'error':'Invalid code'},status=status.HTTP_400_BAD_REQUEST)  
            
            # set password
            user = user[0]
            user.set_password(password)
            user.save()

            # generate tokens for user
            data = send_token_response(user)
            return Response(data,status=status.HTTP_200_OK)
            
        except Exception as e :
            logger.warning(traceback.format_exc())
            return Response({'error':str(e)},status=status.HTTP_400_BAD_REQUEST)  
    
