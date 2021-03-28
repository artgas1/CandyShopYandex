from rest_framework import routers
from CandyShop import viewsets

router = routers.DefaultRouter(trailing_slash=False)
router.register('couriers', viewsets.CourierViewSet, basename='couriers')
router.register('orders', viewsets.OrderViewSet, basename='orders')
