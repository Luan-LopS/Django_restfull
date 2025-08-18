from rest_framework.viewsets import ModelViewSet

from order.models import Order
from order.serializers import order_serializer


class OrderViewSet(ModelViewSet):
    serializer_class = order_serializer
    queryset = Order.objects.all()
