from rest_framework import viewsets
from CandyShop import serializers
from CandyShop import models
from rest_framework import status
from rest_framework.response import Response
from CandyShop import custom_exceptions
from rest_framework.decorators import action
from datetime import datetime
from CandyShop import custom_functions
from django.shortcuts import get_object_or_404


class CourierViewSet(viewsets.ModelViewSet):
    queryset = models.Courier.objects.all()
    serializer_class = serializers.CourierSerializer

    def create(self, request, *args, **kwargs):
        serializer = serializers.CourierListSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def retrieve(self, request, *args, **kwargs):
        courier = get_object_or_404(self.queryset, pk=kwargs.get("pk"))
        serializer = self.serializer_class(courier)
        data = serializer.data
        rating = custom_functions.get_rating(courier)
        if rating is not None:
            data['rating'] = rating
        earnings = custom_functions.get_earnings(courier)
        data['earnings'] = earnings
        return Response(data, status=status.HTTP_200_OK)

    def get_exception_handler(self):
        return custom_exceptions.exception_couriers


class OrderViewSet(viewsets.ModelViewSet):
    queryset = models.Order.objects.all()
    serializer_class = serializers.OrderSerializer

    def create(self, request, *args, **kwargs):
        serializer = serializers.OrderListSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get_exception_handler(self):
        return custom_exceptions.exception_orders

    @action(detail=False, methods=['post'])
    def assign(self, request):
        # Custom validation (if courier_id is passed, if object exists)

        serializer = serializers.AssignSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        courier = models.Courier.objects.get(courier_id=request.data.get("courier_id"))
        courier_orders_weight = [order.weight for order in courier.order_set.filter(complete_time=None)]
        max_weight = custom_functions.convert_courier_type_to_weight(courier.courier_type) - sum(
            courier_orders_weight)

        for order in models.Order.objects.filter(complete_time__isnull=True, courier__isnull=True).order_by("order_id"):
            if order.weight <= max_weight \
                    and order.region in courier.regions \
                    and custom_functions.check_time_intervals(courier.working_hours, order.delivery_hours):
                order = models.Order.objects.get(order_id=order.order_id)
                order.courier = courier
                max_weight -= order.weight

                order.assign_time = datetime.utcnow()
                order.save()
                courier.save()

        if not courier.order_set.exists():
            return Response({"orders": []}, status=200)

        resp = {"orders": []}
        for order in courier.order_set.all():
            if not order.complete_time:
                resp['orders'].append({"id": order.order_id})
        last_successful_assigned_order = courier.order_set.order_by("-assign_time")[0]
        resp.update(
            {"assign_time": custom_functions.convert_datetime_to_iso8601(last_successful_assigned_order.assign_time)})
        return Response(resp, status=200)

    @action(detail=False, methods=['post'])
    def complete(self, request):
        serializer = serializers.CompleteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        order = models.Order.objects.get(order_id=serializer.validated_data.get("order_id"))
        order.complete_time = serializer.validated_data.get("complete_time")
        order.save()

        return Response({"order_id": order.order_id}, status=200)
