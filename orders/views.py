from django_filters import rest_framework as filters
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from orders.serializers import OrderSerializer
from orders.filters import OrderFilter
from diplom.permissions import IsOwner
from rest_framework.viewsets import ModelViewSet
from orders.models import Order


class OrderViewSet(ModelViewSet):

    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = OrderFilter

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Order.objects.all()
        return self.request.user.order_to_user.all()

    def get_permissions(self):
        self.permission_classes = [IsAdminUser]
        if self.action in ['update', 'destroy', 'partial_update']:
            self.permission_classes = [IsOwner]
        elif self.action in ['create', 'list', 'retrieve']:
            self.permission_classes = [IsAuthenticated | IsAdminUser]
        return super(self.__class__, self).get_permissions()
