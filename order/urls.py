from django.urls import path
from . import views

urlpatterns = [
    path('', views.CartDetail.as_view(), name='cart-detail'),
    path('add-product/<int:pk>', views.AddProduct.as_view(), name='add-product-cart'),
    path('delete-item/<str:id>', views.DeleteItemCart.as_view(), name='delete-item-cart'),
    path('checkout/', views.CheckoutView.as_view(), name='checkout-cart'),
]

