from django.urls import path
from .views import RegisterViewSet,VerifyEmailViewSet,LoginViewSet,ForgetPasswordViewSet,ResetPasswordViewSet

urlpatterns = [
    path('register/',RegisterViewSet.as_view(),name='register'),
    path('login/',LoginViewSet.as_view(),name='login'),
    path('verify-email/',VerifyEmailViewSet.as_view(),name='verify_email'),
    path('forget-password/<email>',ForgetPasswordViewSet.as_view(),name='forget_password'),
    path('reset-password/',ResetPasswordViewSet.as_view(),name='reset_password'),
]
