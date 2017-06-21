from rest_framework import viewsets

from . import models
from . import serializers


class FacultyViewSet(viewsets.ModelViewSet):
    """
    Faculties.
    """

    queryset = models.Faculty.objects.all()
    serializer_class = serializers.FacultySerializer


class CourseViewSet(viewsets.ModelViewSet):
    """
    Courses.
    """

    queryset = models.Course.objects.all()
    serializer_class = serializers.CourseSerializer


class DisciplinesViewSet(viewsets.ModelViewSet):
    """
    Disciplines.
    """

    queryset = models.Discipline.objects.all()
    serializer_class = serializers.DisciplineSerializer
