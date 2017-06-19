from rest_framework import serializers

from . import models


class ScoreSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializes the global score of each user.
    """

    class Meta:
        model = models.Score
        fields = 'url', 'user', 'points'


class GivenPointsSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializes given point objects.
    """

    class Meta:
        model = models.GivenPoints
        fields = 'url', 'user', 'token', 'index', 'points'
