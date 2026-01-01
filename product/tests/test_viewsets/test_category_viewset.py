import json
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token
from django.urls import reverse
from ..factories import CategoryFactory, ProductFactory
from order.tests.factories import UserFactory
from product.models import Product, Category


class TestCategoryViewSet(APITestCase):
    client = APIClient()

    def setUp(self):
        self.user = UserFactory()
        token = Token.objects.create(user=self.user)
        token.save()
        self.category = CategoryFactory(title="books")

    def test_get__all_category(self):
        token = Token.objects.get(user__username=self.user.username)
        self.client.credentials(HTTP_AUTHRIZATION="Token " + token.key)
        response = self.client.get(reverse("category-list", kwargs={"version": "v1"}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # import pdb; pdb.set_trace() debug

        category_data = json.loads(response.content)
        self.assertEqual(category_data["results"][0]["title"], self.category.title)
        # title',#'slug',#'description',#'active'

    def test_create_category(self):
        token = Token.objects.get(user__username=self.user.username)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
        data = {
            "title": "teste",
            "slug": "01",
            "description": "testes teste",
            "active": True,
        }

        # import pdb; pdb.set_trace() #debug

        response = self.client.post(
            reverse("category-list", kwargs={"version": "v1"}), data=data, format="json"
        )
        print("Status Code:", response.status_code)
        print("Response content:", response.json())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        created_category = Category.objects.get(title="teste")
        self.assertEqual(created_category.title, "teste")
