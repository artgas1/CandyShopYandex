from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _

import django.contrib.postgres.fields as modelsp


class Courier(models.Model):
    class CourierType(models.TextChoices):
        FOOT = 'foot', _('Пеший курьер')
        BIKE = 'bike', _('Велокурьер')
        CAR = 'car', _('Курьер на автомобиле')

    courier_id = models.IntegerField(unique=True, validators=[MinValueValidator(1)], primary_key=True)
    courier_type = models.CharField(max_length=4, choices=CourierType.choices)
    regions = modelsp.ArrayField(models.IntegerField(), blank=False)
    working_hours = modelsp.ArrayField(models.CharField(max_length=11), blank=False)

    def __str__(self):
        return "courier_id:{}".format(self.courier_id)


class Order(models.Model):
    order_id = models.IntegerField(unique=True, validators=[MinValueValidator(1)], primary_key=True)
    weight = models.FloatField(validators=[MinValueValidator(0.01), MaxValueValidator(50)])
    region = models.IntegerField()
    delivery_hours = modelsp.ArrayField(models.CharField(max_length=11), blank=False)
    courier = models.ForeignKey(Courier, on_delete=models.SET_NULL, null=True, blank=True)
    assign_time = models.DateTimeField(null=True, blank=True)
    complete_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return "order_id:{} | courier:{}".format(self.order_id,
                                                 self.courier)
