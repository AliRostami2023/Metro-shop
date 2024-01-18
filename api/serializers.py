from rest_framework import serializers
from account.models import User
from blog.models import Article
from order.models import Order, OrderItem
from product.models import Product


class UserListSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']
        extra_kwargs = {
            'password': {'read_only': True}
        }


class UserCreatSerializers(serializers.ModelSerializer):
    confirm_password = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password', 'confirm_password']
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'username': {'required': True},
            'email': {'required': True},
            'password': {'required': True, 'write_only': True},
        }

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError('password and confirm must match!')
        return data

    def validate_username(self, value):
        if len(value) < 8:
            raise serializers.ValidationError('username must include 8 number or char!')
        return value

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError('password must include 8 number or char!')
        return value


class ProductListSerializers(serializers.ModelSerializer):
    category = serializers.StringRelatedField(many=True)
    brand = serializers.StringRelatedField()
    color = serializers.StringRelatedField(many=True)
    size = serializers.StringRelatedField(many=True)
    rating = serializers.StringRelatedField(many=True)

    class Meta:
        model = Product
        fields = '__all__'


class ProductCreateSerializers(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class BlogListSerializers(serializers.ModelSerializer):
    category = serializers.StringRelatedField(many=True)
    author = serializers.StringRelatedField()

    class Meta:
        model = Article
        fields = '__all__'


class OrderListSerializers(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Order
        fields = '__all__'


class OrderItemSerializers(serializers.ModelSerializer):
    order = serializers.StringRelatedField()
    product = serializers.StringRelatedField()

    class Meta:
        model = OrderItem
        fields = '__all__'


