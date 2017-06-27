from rest_framework import serializers

from . import models

model_serializer = serializers.HyperlinkedModelSerializer


class FileFormatSerializer(model_serializer):
    """
    Serialize FileFormat instances.
    """

    class Meta:
        model = models.ProgrammingLanguage
        fields = ('url', 'ref', 'name', 'comments', 'is_binary',
                  'is_language', 'is_supported')


class ProgrammingLanguageSerializer(model_serializer):
    """
    Serialize ProgrammingLanguage instances.
    """

    class Meta:
        model = models.ProgrammingLanguage
        fields = ('url', 'ref', 'name', 'comments', 'is_supported')
