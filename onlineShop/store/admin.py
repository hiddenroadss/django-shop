from django.contrib import admin

from store.models import Product, Customer, Order, OrderItem, ShippingAddress


class OrderInLine(admin.StackedInline):
    model = Order
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'is_digit']


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['user', 'email']
    inlines = [OrderInLine]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['customer', 'order_dt', 'is_completed']
    list_editable = ['is_completed']


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity']


@admin.register(ShippingAddress)
class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = ['customer', 'order', 'city']
