from rest_framework import viewsets

from . import models
from . import serializers


class ScoreViewSet(viewsets.ReadOnlyModelViewSet):
    """
    (BETA)

    Score measures the overall activity and achievements accomplished in the
    Codeschool platform.
    """

    queryset = models.Score.objects.all()
    serializer_class = serializers.ScoreSerializer


class GivenPointsViewSet(viewsets.ReadOnlyModelViewSet):
    """
    (BETA)

    Tracks points given to each activity on the codeschool platform.
    """

    queryset = models.GivenPoints.objects.all()
    serializer_class = serializers.GivenPointsSerializer
