from django.test import TestCase
from django.contrib.auth.models import User
from order.serializers.order_serializer import OrderSerializer
from order.tests.factories import OrderFactory
from product.tests.factories import ProductFactory


class TestOrderSerializer(TestCase):
    def test_order_serialization(self):
        product1 = ProductFactory(price=240)
        product2 = ProductFactory(price=4400)

        order = OrderFactory(products=[product1, product2])

        serializer = OrderSerializer(order)
        data = serializer.data

        self.assertEqual(data["user"], order.user.id)

        self.assertEqual(data["total"], product1.price + product2.price)
        self.assertEqual(len(data["products"]), 2)
        self.assertEqual(data["products"][0]["title"], product1.title)
