from rest_framework import viewsets

from . import models
from . import serializers


class KanbanViewSet(viewsets.ModelViewSet):
    """
    Active Kanban boards in the Codeschool platform.
    """

    queryset = models.Kanban.objects.all()
    serializer_class = serializers.KanbanSerializer
