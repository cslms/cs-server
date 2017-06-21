from rest_framework import serializers
from friendship import models


class FriendshipRequestSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer FriendshipRequests models.
    """

    class Meta:
        model = models.FriendshipRequest
        fields = ('url', 'from_user', 'to_user', 'message', 'created',
                  'rejected', 'viewed')


class FriendSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer Friend models.
    """

    class Meta:
        model = models.Friend
        fields = ('url', 'from_user', 'to_user', 'created')


class FollowSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for Follow models.
    """

    class Meta:
        model = models.Follow
        fields = ('url', 'follower', 'followee', 'created')