from .views import *
from django.urls import path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('category',CategoryViewSet,basename='category')

urlpatterns = [
    path('product/<uuid:productId>/',ProductViewSet.as_view(),name='product'),
   
]
urlpatterns+=router.urls
