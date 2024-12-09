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



ZIBAL_BASE_URL = "https://gateway.zibal.ir" if not settings.ZIBAL_SANDBOX else "https://sandbox.zibal.ir"
ZIBAL_API_REQUEST = f"{ZIBAL_BASE_URL}/v1/request"
ZIBAL_API_VERIFY = f"{ZIBAL_BASE_URL}/v1/verify"
ZIBAL_API_STARTPAY = f"{ZIBAL_BASE_URL}/start/"


@login_required
def send_request(request, pk):
    order = Order.objects.get(id=pk, user=request.user)
    product = Product.objects.get(id=pk)

    # ذخیره اطلاعات در سشن برای استفاده در مرحله تأیید پرداخت
    request.session['order_id'] == str(order.id)
    request.session['product_id'] == str(product.id)

    print(f"Session Order ID (after setting): {request.session.get('order_id')}")
    print(f"Session Product ID (after setting): {request.session.get('product_id')}")


    # URL بازگشت
    callback_url = request.build_absolute_uri('/cart/verify-payment/')
    print(f"Callback URL: {callback_url}")

    # داده‌های درخواست به زیبال
    data = {
        "merchant": settings.ZIBAL_MERCHANT,  # Merchant ID از تنظیمات
        "amount": order.total_price,  # مبلغ به ریال
        "callbackUrl": callback_url,  # URL بازگشت
        "description": f"پرداخت سفارش شماره {order.id}",
    }
    try:
        # ارسال درخواست به زیبال
        response = requests.post(ZIBAL_API_REQUEST, json=data, timeout=10)
        print(f"Zibal Request Data: {data}")
        print(f"Zibal Response: {response.json()}")

    
        if response.status_code == 200:
            response_data = response.json()
            if response_data["result"] == 100:  # موفقیت
                return redirect(ZIBAL_API_STARTPAY + str(response_data["trackId"]))
            else:
                return HttpResponse(f"خطا در درخواست پرداخت: {response_data['message']}")
        else:
            return HttpResponse("خطا در اتصال به درگاه زیبال")
    except requests.exceptions.RequestException as e:
        return HttpResponse(f"خطا: {str(e)}")



@login_required
def verify_payment(request):
    # دریافت مقادیر از سشن
    order_id = request.session.get('order_id')
    product_id = request.session.get('product_id')
    track_id = request.GET.get("trackId")

    print(f"Order ID: {order_id}")
    print(f"Product ID: {product_id}")
    print(f"Track ID: {track_id}")

    if not order_id or not product_id or not track_id:
        return HttpResponse("اطلاعات پرداخت ناقص است!")

    # بازیابی سفارش و محصول
    order = get_object_or_404(Order, id=int(order_id))
    product = get_object_or_404(Product, id=int(product_id))

    # داده‌های تأیید پرداخت
    data = {
        "merchant": settings.ZIBAL_MERCHANT,  # Merchant ID
        "trackId": track_id,  # شناسه تراکنش
    }

    try:
        # ارسال درخواست تأیید به زیبال
        response = requests.post(ZIBAL_API_VERIFY, json=data, timeout=10)

        if response.status_code == 200:
            response_data = response.json()
            if response_data["result"] == 100:  # تأیید موفق
                # بروزرسانی وضعیت سفارش و محصول
                order.is_paid = True
                product.availability -= 1
                order.save()
                product.save()

                return HttpResponse(f"پرداخت با موفقیت انجام شد. کد رهگیری: {response_data['refNumber']}")
            else:
                return HttpResponse(f"پرداخت ناموفق: {response_data['message']}")
        else:
            return HttpResponse("خطا در اتصال به سرویس تأیید پرداخت زیبال")
    except requests.exceptions.RequestException as e:
        return HttpResponse(f"خطا: {str(e)}")



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

    