import json
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from ..factories import CategoryFactory, ProductFactory
from product.models import Product, Category


class TestCategoryViewSet(APITestCase):
    client = APIClient()

    def setUp(self):
        self.category = CategoryFactory(title='books')

    def test_get__all_category(self):
        response = self.client.get(
            reverse('category-list', kwargs={'version': 'v1'})
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        category_data = json.loads(response.content)[0]
        self.assertEqual(category_data['title'], self.category.title)
        #self.assertEqual(product_data['slug'], )

         #title',
         #'slug',
         #'description',
         #'active'

    def test_create_category(self):
        data = {
                'title': 'teste',
                'slug': '01',
                'description': 'testes teste',
                'active': True
        }

        #import pdb; pdb.set_trace() debug

        response = self.client.post(
            reverse('category-list', kwargs={'version': 'v1'}),
            data=data,
            format='json'
        )
        print("Status Code:", response.status_code)
        print("Response content:", response.json())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        created_category = Category.objects.get(title='teste')
        self.assertEqual(created_category.title, 'teste')
