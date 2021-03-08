from django_filters import rest_framework as filters
from review.models import Review


class ReviewFilter(filters.FilterSet):

    created_at = filters.DateFromToRangeFilter()

    class Meta:
        model = Review
        fields = ('creator', 'product', 'created_at')
