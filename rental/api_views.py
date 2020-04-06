import django_filters
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from rest_framework_extensions.mixins import NestedViewSetMixin
from .permissions import IsOwner
from . import models
from . import pagination
from . import serializers


class FriendViewset(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = models.Friend.objects.none()
    # queryset = models.Friend.objects.with_overdue()
    pagination_class = pagination.HeaderLimitOffsetPagination
    serializer_class = serializers.FriendSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        user = self.request.user
        return models.Friend.objects.filter(owner=user).with_overdue()


class BelongingViewset(viewsets.ModelViewSet):
    queryset = models.Belonging.objects.none()
    pagination_class = pagination.HeaderLimitOffsetPagination
    serializer_class = serializers.BelongingSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        user = self.request.user
        return models.Belonging.objects.filter(owner=user).with_borrowed()


class BorrowedFilterSet(django_filters.FilterSet):
    missing = django_filters.BooleanFilter(field_name='returned', lookup_expr='isnull')
    overdue = django_filters.BooleanFilter(field_name='returned', method='get_overdue')

    class Meta:
        model = models.Borrowed
        fields = ['what', 'to_who', 'missing', 'overdue']

    def get_overdue(self, queryset, field_name, value):
        if value:
            return queryset.overdue()
        return queryset


class BorrowedViewset(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = models.Borrowed.objects.none()
    serializer_class = serializers.BorrowedSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    filterset_class = BorrowedFilterSet

    def get_queryset(self):
        user = self.request.user
        return models.Borrowed.objects.filter(owner=user)

