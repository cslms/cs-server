from rest_framework import serializers

from . import models

model_serializer = serializers.HyperlinkedModelSerializer


class ConfigOptionKeyValuePairSerializer(model_serializer):
    """
    Serialize ConfigOptionKeyValuePair instances.
    """

    class Meta:
        model = models.ConfigOptionKeyValuePair
        fields = ('name', 'value', 'type')


class DataEntryKeyValuePair(model_serializer):
    """
    Serialize DataEntryKeyValuePair instances.
    """

    class Meta:
        model = models.DataEntryKeyValuePair
        fields = ('name', 'value', 'type')
