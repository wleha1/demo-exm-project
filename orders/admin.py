from django.contrib import admin
from .models import OrderStatus, PickupPoint, Order, OrderItem


@admin.register(OrderStatus)
class OrderStatusAdmin(admin.ModelAdmin):
    ...


@admin.register(PickupPoint)
class PickupPointAdmin(admin.ModelAdmin):
    ...


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'customer', 'status', 'order_date')


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    ...
