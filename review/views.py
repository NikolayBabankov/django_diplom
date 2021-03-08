from diplom.permissions import IsOwner, IsSuperUser
from django_filters import rest_framework as filters
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from review.models import Review
from review.serializers import ReviewSerializer
from review.filter import ReviewFilter


class ReviewViewSet(ModelViewSet):

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = ReviewFilter

    def get_permissions(self):
        self.permission_classes = [IsSuperUser]
        if self.action in ['update', 'destroy', 'partial_update']:
            self.permission_classes = [IsOwner]
        elif self.action == 'create':
            self.permission_classes = [IsAuthenticated]
        elif self.action in ['list', 'retrieve']:
            self.permission_classes = [AllowAny]

        return super(self.__class__, self).get_permissions()
