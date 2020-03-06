from rest_framework import viewsets
from .permissions import IsOwner
from . import models
from . import serializers


class FriendViewset(viewsets.ModelViewSet):
    queryset = models.Friend.objects.none()
    #queryset = models.Friend.objects.with_overdue()
    serializer_class = serializers.FriendSerializer
    permission_classes = [IsOwner]

    def get_queryset(self):
        user = self.request.user
        return models.Friend.objects.filter(owner=user).with_overdue()


class BelongingViewset(viewsets.ModelViewSet):
    queryset = models.Belonging.objects.none()
    serializer_class = serializers.BelongingSerializer
    permission_classes = [IsOwner]

    def get_queryset(self):
        user = self.request.user
        return models.Belonging.objects.filter(owner=user)


class BorrowedViewset(viewsets.ModelViewSet):
    queryset = models.Borrowed.objects.none()
    serializer_class = serializers.BorrowedSerializer
    permission_classes = [IsOwner]

    def get_queryset(self):
        user = self.request.user
        return models.Borrowed.objects.filter(owner=user)

