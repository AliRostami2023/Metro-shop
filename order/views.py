from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import View
from order.cart import Cart
from order.forms import CheckoutForm
from order.models import Order, OrderItem
from product.models import Product
import json
import requests
from account.models import User

MERCHANT = 'test'
ZP_API_REQUEST = "https://api.zarinpal.com/pg/v4/payment/request.json"
ZP_API_VERIFY = "https://api.zarinpal.com/pg/v4/payment/verify.json"
ZP_API_STARTPAY = "https://www.zarinpal.com/pg/StartPay/{authority}"
amount = 0  # Rial / Required
email = ''  # Optional
mobile = ''  # Optional
description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"
CallbackURL = 'http://127.0.0.1:8000/order/verify'


@login_required
def send_request(request, pk):
    order = get_object_or_404(Order, id=pk, user=request.user)
    product = get_object_or_404(Product, id=pk)
    order.save()
    request.session['order_id'] = str(order.id)
    request.session['product_id'] = str(product.id)

    data = {
        "MerchantID": MERCHANT,
        "Amount": order.total_price,
        "Description": description,
        # "Phone": phone,
        "CallbackURL": CallbackURL,
    }
    data = json.dumps(data)
    # set content length by data
    headers = {'content-type': 'application/json', 'content-length': str(len(data))}
    try:
        response = requests.post(ZP_API_REQUEST, data=data, headers=headers, timeout=10)

        if response.status_code == 200:
            response = response.json()
            if response['Status'] == 100:
                return {'status': True, 'url': ZP_API_STARTPAY + str(response['Authority']),
                        'authority': response['Authority']}
            else:
                return {'status': False, 'code': str(response['Status'])}
        return response

    except requests.exceptions.Timeout:
        return {'status': False, 'code': 'timeout'}
    except requests.exceptions.ConnectionError:
        return {'status': False, 'code': 'connection error'}


@login_required
def verify(request, authority):
    order_id = request.session['order_id']
    order = Order.objects.get(id=int(order_id))
    product_id = request.session['product_id']
    product = Product.objects.get(id=product_id)

    data = {
        "MerchantID": MERCHANT,
        "Amount": order.total_price,
        "Authority": authority,
    }
    data = json.dumps(data)
    # set content length by data
    headers = {'content-type': 'application/json', 'content-length': str(len(data))}
    response = requests.post(ZP_API_VERIFY, data=data, headers=headers)

    if response.status_code == 200:
        response = response.json()
        if response['Status'] == 100:
            order.is_paid = True
            product.availability -= 1
            order.save()
            product.save()

            return {'status': True, 'RefID': response['RefID']}
        else:
            return {'status': False, 'code': str(response['Status'])}
    return response


class CartDetail(View):
    def get(self, request):
        cart = Cart(request)
        product = Product.objects.all()
        return render(request, 'order/cart-detail.html', {'cart': cart, 'product': product})


class AddProduct(View):
    def post(self, request: HttpRequest, pk):
        product = Product.objects.get(id=pk)
        color, size, quantity = request.POST.get('color'), request.POST.get('size'), request.POST.get('p_quantity')
        cart = Cart(request)
        cart.add(quantity, size, color, product)
        return redirect(reverse('cart-detail'))


class DeleteItemCart(View):
    def get(self, request, id):
        cart = Cart(request)
        cart.delete_item(id)
        return redirect(reverse('cart-detail'))


class CheckoutView(LoginRequiredMixin, View):
    def get(self, request: HttpRequest):
        cart = Cart(request)
        form = CheckoutForm()
        return render(request, 'order/checkout.html', {'form': form, 'cart': cart})

    def post(self, request: HttpRequest):
        cart = Cart(request)
        form = CheckoutForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            order = Order.objects.create(user=request.user,
                                         total_price=cart.total(),
                                         first_name=cd['first_name'],
                                         last_name=cd['last_name'],
                                         email=cd['email'],
                                         phone_number=cd['phone_number'],
                                         country=cd['country'],
                                         state=cd['state'],
                                         city=cd['city'],
                                         zip_code=cd['zip_code'],
                                         address=cd['address']
                                         )
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    size=item['size'],
                    color=item['color'],
                    quantity=item['quantity'],
                    price=item['price'],
                )
            cart.remove_cart()
            return redirect(reverse('request'))
        return render(request, 'order/checkout.html', {'form': form})
