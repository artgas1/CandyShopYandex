from django.db import models
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _

import django.contrib.postgres.fields as modelsp


class Courier(models.Model):
    class CourierType(models.TextChoices):
        FOOT = 'foot', _('Пеший курьер')
        BIKE = 'bike', _('Велокурьер')
        CAR = 'car', _('Курьер на автомобиле')

    courier_id = models.IntegerField(unique=True, validators=[MinValueValidator(1)], primary_key=True, editable=False)
    courier_type = models.CharField(max_length=4, choices=CourierType.choices)
    regions = modelsp.ArrayField(models.IntegerField())
    working_hours = modelsp.ArrayField(models.TimeField())
