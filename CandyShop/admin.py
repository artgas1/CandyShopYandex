from django.contrib import admin
from CandyShop import models

# Register your models here.

from django.apps import apps

apps_models = apps.get_models()


class OrderAdmin(admin.ModelAdmin):
    model = models.Order
    list_display = [field.name for field in model._meta.get_fields()]


class CourierAdmin(admin.ModelAdmin):
    model = models.Courier
    list_display = [field.name for field in model._meta.get_fields()[1:]]


admin.site.register(models.Order, OrderAdmin)
admin.site.register(models.Courier, CourierAdmin)

for model in apps_models:
    try:
        admin.site.register(model)
    except admin.sites.AlreadyRegistered:
        pass
