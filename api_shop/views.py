from django.shortcuts import render
from django_filters import rest_framework as filters
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated,IsAdminUser,AllowAny,BasePermission
from api_shop.permissions import IsOwner, IsSuperUser
from api_shop.filter import ProductFilter,ReviewFilter,OrderFilter
from api_shop.serializers import OrderSerializer, ProductSerializer,ReviewSerializer, CollectionSerializer
from rest_framework.viewsets import ModelViewSet
from api_shop.models import Product, Review, Order, OrderItem,Collection


class OrderViewSet(ModelViewSet):

    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    
    filter_backends = [filters.DjangoFilterBackend]
    filter_class = OrderFilter

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Order.objects.all()
        return self.request.user.order_to_user.all()

    def get_permissions(self):
        self.permission_classes = [IsSuperUser]
        if self.action in ['update','destroy','partial_update']:
            self.permission_classes = [IsOwner]
        elif self.action in ['create','list','retrieve']:
            self.permission_classes = [IsAuthenticated]
        return super(self.__class__, self).get_permissions()


class ProductViewSet(ModelViewSet):

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filter_class = ProductFilter

    def get_permissions(self):
        if self.action in ['create' ,'update', 'partial_update','destroy']:
            self.permission_classes = [IsAdminUser]
        else:
            self.permission_classes = [AllowAny]
        return [permission() for permission in self.permission_classes]
        


class ReviewViewSet(ModelViewSet):

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    filter_backends = [filters.DjangoFilterBackend]
    filter_class = ReviewFilter
    
    def get_permissions(self):
        self.permission_classes = [IsSuperUser]
        if self.action in ['update','destroy','partial_update']:
            self.permission_classes = [IsOwner]
        elif self.action == 'create':
            self.permission_classes = [IsAuthenticated]
        elif self.action in ['list','retrieve']:
            self.permission_classes = [AllowAny]

        return super(self.__class__, self).get_permissions()



class CollectionViewSet(ModelViewSet):

    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer

    def get_permissions(self):
        if self.action in ['create' ,'update', 'partial_update','destroy']:
            self.permission_classes = [IsAdminUser]
        else:
            self.permission_classes = [AllowAny]
        return [permission() for permission in self.permission_classes]