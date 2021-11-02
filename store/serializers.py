from rest_framework import serializers
from rest_framework.settings import import_from_string

from .models import *

from accounts.serializers import UserSerializer


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug"]
        # exclude = ['slug']


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ["image", "alt_text"]


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    product_image = ImageSerializer(many=True, read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = "__all__"
        # exclude = ["created_at", "updated_at"]


class ShippingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingAddress
        fields = "__all__"


class OrderItemSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        # fields = "__all__"
        fields = [
            "id",
            "created_at",
            "quantity",
            "name",
            "price",
            "image",
            "slug",
            "product",
            "brand",
        ]

    def get_image(self, obj):
        request = self.context.get("request")
        image = obj.image
        return request.build_absolute_uri(image)


class OrderSerializer(serializers.ModelSerializer):
    orderItems = serializers.SerializerMethodField(read_only=True)
    shippingAddress = serializers.SerializerMethodField(read_only=True)
    created_by = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Order
        # fields = "__all__"
        fields = [
            "id",
            "created_by",
            "orderItems",
            "shippingAddress",
            "total_price",
            "total_items",
            "payment_method",
            "shipping_charge",
            "tax",
            "is_paid",
            "is_delivered",
            "paid_at",
            "delivered_at",
            "created_at",
        ]

    def get_orderItems(self, obj):
        request = self.context.get("request")
        items = obj.orderitem_set.all()
        serializer = OrderItemSerializer(items, many=True, context={"request": request})
        return serializer.data

    def get_shippingAddress(self, obj):
        try:
            address = ShippingAddressSerializer(obj.shippingaddress, many=False).data
        except:
            address = False
        return address

    def get_created_by(self, obj):
        user = obj.created_by
        serializer = UserSerializer(user, many=False)
        return serializer.data
