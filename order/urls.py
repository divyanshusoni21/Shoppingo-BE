from .views import *

from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('order',OrderViewSet,basename='order')


urlpatterns = router.urls