from rest_framework import routers
from CandyShop import viewsets

router = routers.DefaultRouter()
router.register('couriers', viewsets.CourierViewSet, basename='couriers')
router.register('orders', viewsets.OrderViewSet, basename='orders')
