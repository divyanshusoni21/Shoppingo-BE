from .views import *
from django.urls import path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('category',CategoryViewSet,basename='category')
router.register('cart',UserCartViewSet,basename='cart')

urlpatterns = [
    path('product/<str:productSlug>/',ProductViewSet.as_view(),name='product'),
    path('product-review/',ProductReviewViewSet.as_view(),name='product_review'),
    path('search/<str:query>/',SearchViewSet.as_view(),name='search'),

   
]
urlpatterns+=router.urls
