from django.core.paginator import Paginator
from django.utils.crypto import get_random_string
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from account.models import User
from api.serializers import UserListSerializers, UserCreatSerializers, ProductListSerializers, BlogListSerializers, \
    OrderListSerializers, OrderItemSerializers, ProductCreateSerializers
from rest_framework import generics, permissions
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from blog.models import Article
from order.models import Order, OrderItem
from product.models import Product


# Create your views here.


class UserListApiView(APIView):
    permission_classes = [IsAdminUser, IsAuthenticated]

    def get(self, request):
        queryset = User.objects.all()
        page_number = self.request.query_params.get('page', 1)
        page_size = self.request.query_params.get('limit', 1)
        paginator = Paginator(queryset, page_size)
        ser_data = UserListSerializers(instance=paginator.page(page_number), many=True)
        return Response(ser_data.data, status.HTTP_200_OK)


class UserCreateApiView(APIView):
    def post(self, request):
        ser_data = UserCreatSerializers(data=request.data)
        if ser_data.is_valid():
            new_user: User = User()
            new_user.first_name = ser_data.validated_data.get('first_name')
            new_user.last_name = ser_data.validated_data.get('last_name')
            new_user.username = ser_data.validated_data.get('username')
            new_user.email = ser_data.validated_data.get('email')
            new_user.set_password(ser_data.validated_data.get('password'))
            new_user.save()
            return Response(ser_data.data, status.HTTP_201_CREATED)
        return Response(ser_data.errors, status.HTTP_400_BAD_REQUEST)


class ProductListApiView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializers


class ProductCreateApiView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Product.objects.all()
    serializer_class = ProductCreateSerializers


class ProductUpdateApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializers


class BlogListApiView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Article.objects.all()
    serializer_class = BlogListSerializers


class BlogCreateApiView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Article.objects.all()
    serializer_class = BlogListSerializers


class BlogUpdateApiView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Article.objects.all()
    serializer_class = BlogListSerializers


class OrderListApiView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Order.objects.all()
    serializer_class = OrderListSerializers


class OrderCreateApiView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Order.objects.all()
    serializer_class = OrderListSerializers


class OrderUpdateApiView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Order.objects.all()
    serializer_class = OrderListSerializers


class OrderItemListApiView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializers


class OrderItemCreateApiView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializers


class OrderItemUpdateApiView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializers
