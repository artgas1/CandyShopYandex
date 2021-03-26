from rest_framework import viewsets
from CandyShop import serializers
from CandyShop import models
from rest_framework import status
from rest_framework.response import Response
from CandyShop import custom_exceptions


class CourierViewSet(viewsets.ModelViewSet):
    queryset = models.Courier.objects.all()
    serializer_class = serializers.CourierSerializer

    def create(self, request, *args, **kwargs):
        serializer = serializers.CourierListSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get_exception_handler(self):
        return custom_exceptions.exception_couriers
