from rest_framework import viewsets

from . import serializers
from .models import Classroom


#
# API Views
#
class ClassroomViewSet(viewsets.ModelViewSet):
    """
    List of classrooms.
    """

    queryset = Classroom.objects.all()
    serializer_class = serializers.ClassroomSerializer
