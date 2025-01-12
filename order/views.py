from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import View
from django.conf import settings
from order.cart import Cart
import datetime
import requests
from order.forms import CheckoutForm, CouponFormField
from order.models import Order, OrderItem, Coupon
from product.models import Product




from django.conf import settings
import requests
import json


#? sandbox merchant 
if settings.SANDBOX:
    sandbox = 'sandbox'
else:
    sandbox = 'www'


ZP_API_REQUEST = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
ZP_API_VERIFY = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
ZP_API_STARTPAY = f"https://{sandbox}.zarinpal.com/pg/StartPay/"

amount = 1000  # Rial / Required
description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"  # Required
phone = 'YOUR_PHONE_NUMBER'  # Optional
CallbackURL = 'http://127.0.0.1:8080/cart/verify/'


class RequestPayment(View):
    def post(self, request, pk, product_id):
        order = get_object_or_404(Order, id=pk, user=request.user)
        product = get_object_or_404(Product, id=product_id)
        order.save()
        product.save()

        request.session['order_id'] = str(order.id)
        request.session['product_id'] = str(product.id)

        data = {
            "MerchantID": settings.MERCHANT,
            "Amount": order.total_price *10,
            "Description": description,
            "Phone": phone,
            "CallbackURL": CallbackURL,
        }
        data = json.dumps(data)
        headers = {'content-type': 'application/json', 'content-length': str(len(data)) }
        try:
            response = requests.post(ZP_API_REQUEST, data=data,headers=headers, timeout=10)

            if response.status_code == 200:
                response = response.json()
                if response['Status'] == 100:
                    return {'status': True, 'url': ZP_API_STARTPAY + str(response['Authority']), 'authority': response['Authority']}
                else:
                    return {'status': False, 'code': str(response['Status'])}
            return response
    
        except requests.exceptions.Timeout:
            return {'status': False, 'code': 'timeout'}
        except requests.exceptions.ConnectionError:
            return {'status': False, 'code': 'connection error'}



class VerifyPayment(View):
    def get(self, request, authority):
        order_id = request.session['order_id']
        product_id = request.session['product_id']

        order = Order.objects.get(id=int(order_id))
        product = Product.objects.get(id=int(product_id))

        data = {
            "MerchantID": settings.MERCHANT,
            "Amount": order.total_price * 10,
            "Authority": authority,
        }
        data = json.dumps(data)
        # set content length by data
        headers = {'content-type': 'application/json', 'content-length': str(len(data)) }
        response = requests.post(ZP_API_VERIFY, data=data,headers=headers)

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
    form_class = CouponFormField

    def get(self, request):
        cart = Cart(request)
        product = Product.objects.all()
        return render(request, 'order/cart-detail.html', {'cart': cart, 'product': product, 'form': self.form_class})



class AddProduct(View):
    def post(self, request: HttpRequest, pk):
        product = Product.objects.get(id=pk)
        color, size, quantity = request.POST.get('color'), request.POST.get('size'), request.POST.get('p_quantity')
        cart = Cart(request)
        cart.add(quantity, size, color, product)
        return redirect(product.get_absolute_url())


class DeleteItemCart(View):
    def get(self, request, id):
        cart = Cart(request)
        cart.delete_item(id)
        return redirect(reverse('cart-detail', cart.id))


class CheckoutView(LoginRequiredMixin, View):
    template_name = 'order/checkout.html'
    form_class = CheckoutForm

    def get(self, request: HttpRequest):
        cart = Cart(request)
        form = self.form_class()
        return render(request, self.template_name, {'form': form, 'cart': cart})

    def post(self, request: HttpRequest):
        cart = Cart(request)
        form = self.form_class(request.POST)
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
        return render(request, self.template_name, {'form': form})


class CouponOrderView(LoginRequiredMixin, View):
    form_class = CouponFormField

    def post(self, request):
        now = datetime.datetime.now()
        form = self.form_class(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            try:
                coupon = Coupon.objects.get(code__exact=code, valid_from__lte=now, valid_to__gte=now, active=True)
            except Coupon.DoesNotExist:
                return redirect(reverse('cart-detail'))
            order = Order.objects.get(id=order.id)
            order.discount = coupon.discount
            order.save()
        return redirect(reverse('cart-detail'))

    