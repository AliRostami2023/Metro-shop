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
from django.conf import settings
from account.models import User

if settings.SANDBOX:
    sandbox = 'sandbox'
else:
    sandbox = 'www'

ZP_API_REQUEST = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
ZP_API_VERIFY = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
ZP_API_STARTPAY = f"https://{sandbox}.zarinpal.com/pg/StartPay/"
description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"
CallbackURL = 'http://127.0.0.1:8000/order/verify'


@login_required
def request_payment(request):
    current_order, created = Order.objects.get_or_create(is_paid=False, user_id=request.user.id)
    total_price = current_order.result_total_price()

    if total_price == 0:
        return redirect(reverse('cart-detail'))
    data = {
        "MerchantID": settings.MERCHANT,
        "Amount": total_price,
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
    authority = request.GET['Authority']
    current_order, created = Order.objects.get_or_create(is_paid=False, user_id=request.user.id)
    total_price = current_order.result_total_price()
    # user = User.objects.filter(id=request.user.id).first()

    data = {
        "MerchantID": settings.MERCHANT,
        "Amount": total_price,
        'Authority': authority,

    }
    data = json.dumps(data)
    headers = {'content-type': 'application/json', 'content-length': str(len(data))}

    res = requests.post(ZP_API_VERIFY, data=data, headers=headers)
    if res.status_code == 200:
        response = res.json()

        if response['Status'] == 100:
            current_order.is_paid = True
            current_order.product_item.availability -= 1
            current_order.save()
            return redirect(reverse('order:secces_payment_redirect'))

    return redirect(reverse('order:unsecces_payment_redirect'))


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
                                         address=cd['address'])
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
        return render(request, 'order/checkout.html', {'form': form})
