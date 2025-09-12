from django.test import TestCase
from product.tests.factories import CategoryFactory
from ..factories import ProductFactory
from product.serializers.produtc_serializer import ProductSerializer
from product.serializers.category_serializer import CategorySerializer


class Test_ProductSerializer(TestCase):
    def test_serializationProduct(self):
        product = ProductFactory()
        serializer = ProductSerializer(product)
        data = serializer.data

        self.assertEqual(data['title'], product.title)
        self.assertAlmostEqual(float(data['price']), float(product.price), places=1)
        self.assertEqual(data['category'], list(product.category.values_list('id', flat=True)))


class Teste_CategorySerializer(TestCase):
    def test_serializetionCategory(self):
        category = CategoryFactory()
        serializer = CategorySerializer(category)
        data = serializer.data

        self.assertEqual(data['title'], category.title)
        self.assertEqual(data['slug'], category.slug)
        self.assertEqual(data['description'], category.description)
        self.assertEqual(data['active'], category.active)
