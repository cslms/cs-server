from rest_framework import viewsets

from . import models
from . import serializers


class ProgrammingLanguageViewSet(viewsets.ModelViewSet):
    """
    A ProgrammingLanguage instance represents a programming language
    support inside Codeschool.

    Can be used to personalize source code highlighting or to define the
    programming language of a source code submission.
    """

    queryset = models.ProgrammingLanguage.objects.all()
    serializer_class = serializers.ProgrammingLanguageSerializer


class FileFormatViewSet(viewsets.ModelViewSet):
    """
    A file format that can be used on Codeschool.
    """

    queryset = models.FileFormat.objects.all()
    serializer_class = serializers.FileFormatSerializer
