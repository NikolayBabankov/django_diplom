from django_filters import rest_framework as filters
from catalog.models import Product


class ProductFilter(filters.FilterSet):

    title = filters.CharFilter(lookup_expr='icontains')
    description = filters.CharFilter(lookup_expr='icontains')
    price = filters.RangeFilter()

    class Meta:
        model = Product
        fields = ('id', 'title', 'description', 'price')
