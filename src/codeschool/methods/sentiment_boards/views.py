from rest_framework import viewsets

from . import models
from . import serializers


class SentimentBoardViewSet(viewsets.ModelViewSet):
    """
    Active Kanban boards in the Codeschool platform.
    """

    queryset = models.SentimentBoard.objects.all()
    serializer_class = serializers.SentimentBoardSerializer
