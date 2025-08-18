from rest_framework import serializers
from order.models import Order
from product.serializers.produtc_serializer import ProductSerializer


class OrderSerializer(serializers.ModelSerializer):
    products = ProductSerializer(required=True, many=True)
    products_id = serializers.PrimaryKeyRelatedField(query=products.objects.all(), write_only=True, many=True)
    total = serializers.SerializerMethodField()

    def get_total(self, instance):
        total = sum([product.price for product in instance.products.all()])
        return total

    class Meta:
        model = Order
        fields = ['user', 'products', 'total', 'products_id']
        extra_kwargs = {'product': {'required': False}}

    def create(self, validated_data):
        product_data = validated_data.pop('products_id')
        user_data = validated_data.pop('user')

        order = Order.objects.create(validated_data)
        for product in product_data:
            order.products.add(product)

        return order