from rest_framework import serializers

from . import models


class ActivityListSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializes Activity lists
    """

    sections = serializers.SerializerMethodField()

    class Meta:
        model = models.ActivityList
        fields = 'url', 'id', 'title', 'short_description', 'sections'

    def get_sections(self, obj):
        children = list(obj.get_children())
        ctx = self.context
        return [
            ActivitySectionSerializer(x.specific, context=ctx).data
            for x in children]


class ActivitySectionSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializes Activity lists
    """

    class Meta:
        model = models.ActivitySection
        fields = 'url', 'id', 'title', 'short_description'
