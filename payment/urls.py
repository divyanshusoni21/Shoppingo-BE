from django.urls import path
from .views import PaymentInitializeViewSet,PaymentHandlerViewSet

urlpatterns = [
    path('payment-initialize/',PaymentInitializeViewSet.as_view(),name='payment_initialize'),
    path('payment-handler/',PaymentHandlerViewSet.as_view(),name='payment_handler'),
]
