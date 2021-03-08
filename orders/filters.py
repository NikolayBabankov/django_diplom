from django_filters import rest_framework as filters
from orders.models import Order


class OrderFilter(filters.FilterSet):

    status = filters.CharFilter()
    sum_order = filters.RangeFilter()
    created_at = filters.DateFromToRangeFilter()
    updated_at = filters.DateFromToRangeFilter()

    position_orders = filters.ModelMultipleChoiceFilter(
        queryset=Order.objects.all(),
        field_name='position_orders__title',
        to_field_name='title',
    )

    class Meta:
        model = Order
        fields = (
            'status', 'sum_order',
            'created_at', 'updated_at', 'position_orders__title')
