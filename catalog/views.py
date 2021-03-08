from django_filters import rest_framework as filters
from rest_framework.permissions import IsAdminUser, AllowAny
from catalog.models import Product, Collection
from catalog.serializers import ProductSerializer, CollectionSerializer
from catalog.filter import ProductFilter
from rest_framework.viewsets import ModelViewSet


class ProductViewSet(ModelViewSet):

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = ProductFilter

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAdminUser]
        else:
            self.permission_classes = [AllowAny]
        return [permission() for permission in self.permission_classes]


class CollectionViewSet(ModelViewSet):

    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAdminUser]
        else:
            self.permission_classes = [AllowAny]
        return [permission() for permission in self.permission_classes]
