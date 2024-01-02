from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProductList.as_view(), name='product-list'),
    path('category/<cat>', views.ProductList.as_view(), name='category_url_page'),
    path('brand/<brand>', views.ProductList.as_view(), name='brand_url_page'),
    path('detail/<slug:slug>', views.ProductDetail.as_view(), name='product-detail'),
    path('search/', views.search, name='search-product'),
]

