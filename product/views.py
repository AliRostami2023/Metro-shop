from django.core.paginator import Paginator
from django.db.models import Count
from django.http import HttpRequest
from django.shortcuts import render
from django.views.generic import ListView, DetailView

from product.models import Product, Category, Brand


# Create your views here.


class ProductList(ListView):
    template_name = 'product/product-list.html'
    model = Product
    paginate_by = 8
    context_object_name = 'products'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['product_rating'] = Product.objects.filter(rating__isnull=False).order_by('rating__average')[:3]
        context['product_sale'] = Product.objects.filter(discount__isnull=False).order_by('-discount')[:3]
        return context

    def get_queryset(self):
        query = super().get_queryset()

        category_name = self.kwargs.get('cat')
        brand_name = self.kwargs.get('brand')

        if brand_name is not None:
            query = query.filter(brand__url_title__iexact=brand_name)

        if category_name is not None:
            query = query.filter(category__url_title__iexact=category_name)
        return query


class ProductDetail(DetailView):
    template_name = 'product/product-detail.html'
    model = Product
    context_object_name = 'product'


def product_category_component(request):
    categories = Category.objects.annotate(product_category=Count('category')).filter(published=True,
                                                                                      parent__isnull=True).all()
    return render(request, 'product/components/product-category-component.html', {'categories': categories})


def product_brand_component(request):
    brands = Brand.objects.annotate(product_brand=Count('brand')).filter(published=True).all()
    return render(request, 'product/components/product-brand-component.html', {'brands': brands})


def search(request: HttpRequest):
    q = request.GET.get('q')
    products = Product.objects.filter(title__icontains=q)
    page_number = request.GET.get('page')
    paginator = Paginator(products, 12)
    object_list = paginator.get_page(page_number)
    return render(request, 'product/search-product.html', {'products': object_list})
