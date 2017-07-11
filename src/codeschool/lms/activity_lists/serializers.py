from rest_framework import serializers

from . import models


class ActivityListSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializes Activity lists
    """

    # activities = serializers.SerializerMethodField()

    class Meta:
        model = models.ActivityList
        fields = 'url', 'id', 'name', 'slug', 'short_description'
