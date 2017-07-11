from rest_framework import serializers

from . import models


class KanbanSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serialize Kanban boards.
    """

    class Meta:
        model = models.Kanban
        fields = ('url', 'name', 'members')

