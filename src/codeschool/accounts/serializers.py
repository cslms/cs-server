from rest_framework import serializers
from . import models


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serialize User objects.
    """

    name = serializers.SerializerMethodField()

    class Meta:
        model = models.User
        fields = ('url', 'username', 'email', 'name')

    def get_name(self, obj):
        return obj.first_name + ' ' + obj.last_name
