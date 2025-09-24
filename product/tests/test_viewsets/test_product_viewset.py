import json
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from ..factories import CategoryFactory, ProductFactory
from order.tests.factories import UserFactory
from product.models import Product


class TestProductViewSet(APITestCase):
    client = APIClient()

    def setUp(self):
        self.user = UserFactory()

        self.product = ProductFactory(
            title='pro Controller',
            price=200.00
        )

    def test_get__all_product(self):
        response = self.client.get(
            reverse('product-list', kwargs={'version': 'v1'})
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        product_data = json.loads(response.content)[0]
        self.assertEqual(product_data['title'], self.product.title)
        self.assertEqual(float(product_data['price']), float(self.product.price))
        self.assertEqual(product_data['active'], self.product.active)

    def test_create_product(self):
        category = CategoryFactory()
        data = {
                'title': 'notebook',
                'description': 'teste',
                'price': 800.00,
                'category_id': [category.id],
        }

        response = self.client.post(
            reverse('product-list', kwargs={'version': 'v1'}),
            data=data,
            format='json'
        )
        print("Status Code:", response.status_code)
        print("Response content:", response.json())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        created_product = Product.objects.get(title='notebook')
        self.assertEqual(created_product.title, 'notebook')
        self.assertEqual(created_product.price, 800.00)
