from rest_framework import viewsets

from . import models
from . import serializers


class PairViewSet(viewsets.ModelViewSet):
    """
    A pair of students.
    """

    queryset = models.Pair.objects.all()
    serializer_class = serializers.PairSerializer


class TeamViewSet(viewsets.ModelViewSet):
    """
    A pair of students.
    """

    queryset = models.Team.objects.all()
    serializer_class = serializers.TeamSerializer
