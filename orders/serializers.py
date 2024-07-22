from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Order, OrderProduct
from products.models import Product


class OrderProductSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()

    class Meta:
        model = OrderProduct
        fields = ["product_id", "quantity"]


class OrderSerializer(serializers.ModelSerializer):
    products = OrderProductSerializer(many=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Order
        fields = ["user", "products", "created_at", "status", "order_ref"]

    def create(self, validated_data):
        products_data = validated_data.pop("products")
        order = Order.objects.create(**validated_data)
        print(products_data)
        for product_data in products_data:
            product = Product.objects.get(id=int(product_data["product_id"]))
            OrderProduct.objects.create(
                order=order, product=product, quantity=product_data["quantity"]
            )
        order.calculate_total_amount()
        return order
