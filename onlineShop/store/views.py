import datetime
import json
from decimal import Decimal

from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import ListView

from store.models import Product, Order, OrderItem, Customer, ShippingAddress


class ProductListView(ListView):
    model = Product

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            customer, created = Customer.objects.get_or_create(user=request.user)
            customer.save()
            return super().get(request, *args, **kwargs)


def cart_view(request, *args, **kwargs):
    order_items = OrderItem.objects.filter(order__customer__user=request.user)
    order = Order.objects.get(customer=request.user.customer)
    return render(request, 'store/cart.html', context={'order_items': order_items, 'order': order})


def checkout_view(request, *args, **kwargs):
    order_items = OrderItem.objects.filter(order__customer__user=request.user)
    order = Order.objects.get(customer=request.user.customer)
    return render(request, 'store/checkout.html', context={'order_items': order_items, 'order': order})


def update_cart_view(request, *args, **kwargs):
    data = json.loads(request.body)
    product_id, action = data['productId'], data['action']
    if request.user.is_authenticated:
        order, created = Order.objects.get_or_create(customer=request.user.customer)
        order_item, created = OrderItem.objects.get_or_create(order=order, product_id=product_id)
        if action == 'add':
            order_item.quantity += 1
        elif action == 'remove':
            order_item.quantity -= 1
        order_item.save()
        if order_item.quantity == 0:
            order_item.delete()
    return JsonResponse('We receive data on the back-end', safe=False)


def process_order_view(request, *args, **kwargs):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, is_completed=False)
        total = Decimal(data['user_form']['total'])
        order.transaction_id = transaction_id

        if total == order.get_total_price:
            order.is_completed = True
        order.save()
        if order.need_shipping:
            ShippingAddress.objects.create(customer=customer, order=order, address=data['shipping_form']['address'],
                                           city=data['shipping_form']['city'], state=data['shipping_form']['state'],
                                           zip_code=data['shipping_form']['zipCode'])
    else:
        print('User is not logged in')
    return JsonResponse('Payment complete', safe=False)
