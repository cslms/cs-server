from rest_framework import serializers

from . import models


class FacultySerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializes Faculty objects.
    """

    class Meta:
        model = models.Faculty
        fields = ('url', 'name', 'slug', 'description')


class CourseSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializes Course objects.
    """

    class Meta:
        model = models.Course
        fields = ('url', 'name', 'slug', 'description', 'faculty')


class DisciplineSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializes Discipline objects.
    """

    class Meta:
        model = models.Discipline
        fields = ('url', 'name', 'slug', 'description', 'faculty', 'code',
                  'since', 'syllabus', 'program', 'bibliography')
