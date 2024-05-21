from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('user-list/', views.UserListApiView.as_view()),
    path('create-user/', views.UserCreateApiView.as_view()),
    path('login-user/', views.UserLoginApiView.as_view()),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('product-list/', views.ProductListApiView.as_view()),
    path('product-create/', views.ProductCreateApiView.as_view()),
    path('product-update/<pk>/', views.ProductUpdateApiView.as_view()),
    path('blog-list/', views.BlogListApiView.as_view()),
    path('blog-create/', views.BlogCreateApiView.as_view()),
    path('blog-update/<pk>/', views.BlogUpdateApiView.as_view()),
    path('order-list/', views.OrderListApiView.as_view()),
    path('order-create/', views.OrderCreateApiView.as_view()),
    path('order-update/<pk>/', views.OrderUpdateApiView.as_view()),
    path('order-item-list/', views.OrderItemListApiView.as_view()),
    path('order-item-create/', views.OrderItemCreateApiView.as_view()),
    path('order-item-update/<pk>/', views.OrderItemUpdateApiView.as_view()),
]

