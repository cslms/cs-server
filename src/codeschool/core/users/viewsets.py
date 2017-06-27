from rest_framework import viewsets
from . import models
from . import serializers


class UserViewSet(viewsets.ModelViewSet):
    """
    Active users in the Codeschool platform.
    """

    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer