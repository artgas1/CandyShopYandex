from rest_framework import serializers
from datetime import datetime
from CandyShop import models

time_format = "%H:%M"


class TimeInterval:
    def __init__(self, time):
        try:
            start, end = time.split('-')
            self.start = datetime.strptime(start, time_format)
            self.end = datetime.strptime(end, time_format)
        except Exception:
            raise serializers.ValidationError("Time interval is in incorrect format. Correct format: '%H:%M-%H:%M'")
        if self.start > self.end:
            raise serializers.ValidationError("Start time is greater than date time")

    def __repr__(self):
        return "{}-{}".format(datetime.strftime(self.start, time_format), datetime.strftime(self.end, time_format))

    def __str__(self):
        return "{}-{}".format(datetime.strftime(self.start, time_format), datetime.strftime(self.end, time_format))


class TimeIntervalField(serializers.Field):
    def to_representation(self, value):
        return str(value)

    def to_internal_value(self, data):
        time_string = TimeInterval(data)
        return str(time_string)


class CourierSerializer(serializers.ModelSerializer):
    working_hours = serializers.ListField(child=TimeIntervalField())
    rating = serializers.SerializerMethodField()

    def update(self, instance, validated_data):
        validated_data.pop('courier_id', None)  # prevent courier_id from being updated
        return super().update(instance, validated_data)

    def get_rating(self, courier):
        orders_completed = courier.order_set.filter(complete_time__isnull=False)
        print(orders_completed)

    class Meta:
        model = models.Courier
        fields = ['courier_id', 'courier_type', 'regions', 'working_hours', 'rating']


class CourierListSerializer(serializers.Serializer):
    data = CourierSerializer(many=True)

    def create(self, validated_data):
        couriers_data = validated_data.get('data')
        serializer = CourierSerializer(data=couriers_data, many=True)
        serializer.is_valid(raise_exception=False)
        couriers = serializer.save()
        return {"data": couriers}

    def to_representation(self, instance):
        return {"couriers": [{"id": courier.courier_id} for courier in instance.get("data")]}


class OrderSerializer(serializers.ModelSerializer):
    delivery_hours = serializers.ListField(child=TimeIntervalField())

    def update(self, instance, validated_data):
        validated_data.pop('order_id', None)  # prevent courier_id from being updated
        return super().update(instance, validated_data)

    class Meta:
        model = models.Order
        fields = ['order_id', 'weight', 'region', 'delivery_hours']


class OrderListSerializer(serializers.Serializer):
    data = OrderSerializer(many=True)

    def create(self, validated_data):
        order_data = validated_data.get('data')
        serializer = OrderSerializer(data=order_data, many=True)
        serializer.is_valid(raise_exception=False)
        order = serializer.save()
        return {"data": order}

    def to_representation(self, instance):
        return {"orders": [{"id": order.order_id} for order in instance.get("data")]}


class AssignSerializer(serializers.Serializer):
    courier_id = serializers.IntegerField()

    def validate_courier_id(self, attrs):
        if models.Courier.objects.filter(courier_id=attrs).count():
            return attrs
        raise serializers.ValidationError("Courier with this id does not exist.")


class CompleteSerializer(serializers.Serializer):
    courier_id = serializers.IntegerField()
    order_id = serializers.IntegerField()
    complete_time = serializers.DateTimeField(input_formats=["%Y-%m-%dT%H:%M:%S.%fZ"])

    def validate_courier_id(self, attrs):
        if models.Courier.objects.filter(courier_id=attrs).count():
            return attrs
        raise serializers.ValidationError("Courier with this id does not exist.")

    def validate_order_id(self, attrs):
        if models.Order.objects.filter(order_id=attrs).count():
            return attrs
        raise serializers.ValidationError("Order with this id does not exist.")

    def validate(self, attrs):
        courier = models.Courier.objects.get(courier_id=attrs.get("courier_id"))
        order = models.Order.objects.get(order_id=attrs.get("order_id"))
        if order not in courier.order_set.all():
            raise serializers.ValidationError("Order is not assigned to this courier.")
