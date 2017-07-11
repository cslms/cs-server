from rest_framework import viewsets

from . import models
from . import serializers


class OrganizationViewSet(viewsets.ModelViewSet):
    """
    Organizations.
    """

    queryset = models.Organization.objects.all()
    serializer_class = serializers.OrganizationSerializer


class DisciplinesViewSet(viewsets.ModelViewSet):
    """
    Disciplines.
    """

    queryset = models.Discipline.objects.all()
    serializer_class = serializers.DisciplineSerializer
