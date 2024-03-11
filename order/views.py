from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest
from django.shortcuts import render, redirect
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
amount = 0 # Rial / Required
email = ''  # Optional
mobile = ''  # Optional
description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"
CallbackURL = 'http://127.0.0.1:8000/order/verify'


@login_required
def request_payment(request):
    cart = Cart(request)
    total_price = cart.total()

    if total_price == 0:
        return redirect(reverse('cart-detail'))
    data = {
        "MerchantID": MERCHANT,
        "Amount": total_price * 10,
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
                url = f"{ZP_API_STARTPAY}{response['Authority']}"
                return redirect(url)
            else:
                return {'status': False, 'code': str(response['Status'])}
        return response

    except requests.exceptions.Timeout:
        return {'status': False, 'code': 'timeout'}
    except requests.exceptions.ConnectionError:
        return {'status': False, 'code': 'connection error'}


@login_required
def verify_payment(request):
    cart = Cart(request)
    total_price = cart.total()
    order = Order.objects.filter(user_id=request.user.id).first()
    # user = User.objects.filter(id=request.user.id).first()
    t_authority = request.GET['Authority']

    data = {
        "MerchantID": MERCHANT,
        "Amount": total_price,
        'Authority': t_authority,
    }

    data = json.dumps(data)
    headers = {'content-type': 'application/json', 'content-length': str(len(data))}

    res = requests.post(ZP_API_VERIFY, data=data, headers=headers)
    if res.status_code == 200:
        response = res.json()

        if response['Status'] == 100:
            order.is_paid = True
            order.product_item.availability -= 1
            order.save()
            return redirect(reverse('success_payment'))

    return redirect(reverse('un_success_payment'))


@login_required
def success_payment(request: HttpRequest):
    return render(request, 'order/success-payment.html', {})


@login_required
def un_success_payment(request: HttpRequest):
    return render(request, 'order/un-success-payment.html', {})


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
