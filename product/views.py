from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count
from django.http import HttpRequest
from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import ListView
from .filters import ProductFilter
from product.models import Product, Category, Brand, CommentProduct



class ProductList(ListView):
    template_name = 'product/product-list.html'
    model = Product
    paginate_by = 8
    # context_object_name = 'products'

    
    def get_queryset(self):
        query = super().get_queryset()

        self.filterset = ProductFilter(self.request.GET, queryset=query)

        category_name = self.kwargs.get('cat')
        brand_name = self.kwargs.get('brand')

        if brand_name is not None:
            query = query.filter(brand__url_title__iexact=brand_name)
            return query

        if category_name is not None:
            query = query.filter(category__url_title__iexact=category_name)
            return query
        
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        context['products'] = Product.objects.prefetch_related('category').select_related('brand').filter(published=True)
        context["product_rating"] = Product.objects.filter(rating__isnull=False).order_by('rating__average')[:3]
        context["product_sale"] = Product.objects.filter(discount__isnull=False).order_by('-discount')[:3]
        return context


class ProductDetail(View):
    template_name = 'product/product-detail.html'

    def setup(self, request, *args, **kwargs):
        self.product_single = get_object_or_404(Product, slug=kwargs['slug'])
        return super().setup(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        product = self.product_single
        categories = Category.objects.all()
        related_product = Product.objects.prefetch_related('category').filter(category__in=categories).exclude(pk=product.pk).distinct()
        return render(request, self.template_name, {'product': product, 'related_product': related_product})

    @method_decorator(login_required)
    def post(self, request: HttpRequest, *args, **kwargs):
        product = self.product_single

        parent_id = request.POST.get('parent_id')
        body = request.POST.get('body')
        CommentProduct.objects.create(body=body, product=product, user=request.user, parent_id=parent_id)
        return render(request, self.template_name, {'product': product})


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
