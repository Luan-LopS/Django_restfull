from rest_framework.viewsets import ModelViewSet

from product.models import Category
from product.serializers.produtc_serializer import CategorySerializer


class CategoryViewSet(ModelViewSet):
    serializer_class = CategorySerializer

    def get_queryset(self):
        return Category.objects.all()
