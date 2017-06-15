from friendship import models
from rest_framework import viewsets

from . import serializers


class FriendshipRequestViewSet(viewsets.ModelViewSet):
    """
    Represents a request for friendship.

    Friendship is not yet neither accepted nor rejected.
    """

    queryset = models.FriendshipRequest.objects.all()
    serializer_class = serializers.FriendshipRequestSerializer


class FriendViewSet(viewsets.ModelViewSet):
    """
    Represents a symmetric friendship relation.
    """

    queryset = models.Friend.objects.all()
    serializer_class = serializers.FriendSerializer


class FollowerViewSet(viewsets.ModelViewSet):
    """
    Allow users to follow each other.
    """

    queryset = models.Follow.objects.all()
    serializer_class = serializers.FollowSerializer


class FolloweeViewSet(viewsets.ModelViewSet):
    """
    Allow users to follow each other.
    """

    queryset = models.Follow.objects.all()
    serializer_class = serializers.FollowSerializer
