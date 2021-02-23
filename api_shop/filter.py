from django_filters import rest_framework as filters
from api_shop.models import Product,Review,Order,OrdersChoices

class ProductFilter(filters.FilterSet):
    '''Фильтр для товаров'''

    title = filters.CharFilter(lookup_expr="icontains")
    description = filters.CharFilter(lookup_expr="icontains")
    price = filters.RangeFilter()

    class Meta:
        model=Product
        fields = ("id", "title","description","price")


class ReviewFilter(filters.FilterSet):
    '''Фильтр для отзывов'''

    created_at = filters.DateFromToRangeFilter()

    class Meta:
        model=Review
        fields = ("creator", "product","created_at")

class OrderFilter(filters.FilterSet):
    '''Фильтр для заказов'''

    status = filters.CharFilter()
    sum_order = filters.RangeFilter()
    created_at = filters.DateFromToRangeFilter()
    updated_at = filters.DateFromToRangeFilter()

    pozition_orders = filters.ModelMultipleChoiceFilter(
        queryset = Order.objects.all(),
        field_name="pozition_orders__title",
        to_field_name='title',
    )

    class Meta:
        model=Order
        fields = ("status", "sum_order","created_at","updated_at","pozition_orders__title")
