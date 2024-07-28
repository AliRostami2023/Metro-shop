from django.shortcuts import render
from django.views.generic import TemplateView, CreateView
from blog.models import Article
from home.forms import ContactForm
from home.models import ContactUs
from order.cart import Cart
from product.models import Category, Slider, Product, BannerSite
from site_settings.models import Setting, FooterBox, FooterLink


# Create your views here.


class IndexView(TemplateView):
    template_name = 'home/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['sliders'] = Slider.objects.filter(published=True).all()
        context['banners'] = BannerSite.objects.filter(published=True).all()[:3]
        context['products'] = Product.objects.filter(published=True).order_by('-created')[:10]
        context['product_discount'] = Product.objects.filter(published=True, discount__isnull=False).order_by(
            '-discount')[:10]
        context['product_more_rating'] = Product.objects.filter(published=True, rating__isnull=False).order_by(
            'rating__average')[:7]
        context['blogs'] = Article.objects.order_by('-date')[:6]
        return context


class ContactUsView(CreateView):
    template_name = 'home/contact-us.html'
    model = ContactUs
    form_class = ContactForm
    success_url = '/'


def site_header_component(request):
    cart = Cart(request)
    categories = Category.objects.filter(published=True, is_parent=False).all()
    settings = Setting.objects.filter(active=True).first()
    return render(request, 'shared/site-header-component.html',
                  {'cart': cart, 'categories': categories, 'settings': settings})


def site_footer_component(request):
    settings = Setting.objects.filter(active=True).first()
    footer_box = FooterBox.objects.all()[:3]
    footer_link = FooterLink.objects.all()
    return render(request, 'shared/site-footer-component.html',
                  {'settings': settings, 'footer_box': footer_box, 'footer_link': footer_link})
