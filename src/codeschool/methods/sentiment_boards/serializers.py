from rest_framework import serializers

from . import models


class SentimentBoardSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serialize Kanban boards.
    """

    class Meta:
        model = models.SentimentBoard
        fields = ('url', 'name', 'members', 'features', 'board')

