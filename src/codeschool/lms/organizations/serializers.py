from rest_framework import serializers

from . import models


class OrganizationSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializes Organization objects.
    """

    class Meta:
        model = models.Organization
        fields = ('url', 'name', 'slug', 'description')


class DisciplineSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializes Discipline objects.
    """

    class Meta:
        model = models.Discipline
        fields = ('url', 'name', 'slug', 'description', 'faculty', 'code',
                  'since', 'syllabus', 'program', 'bibliography')
