from rest_framework import serializers

from . import models


class SimplePairSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serialize Pairs excluding any information about original activity.
    """

    class Meta:
        model = models.Pair
        fields = 'name', 'first_student', 'second_student'


class PairSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serialize Pairs, including information about original activity.
    """

    class Meta:
        model = models.Pair
        fields = 'name', 'first_student', 'second_student', 'activity'


class SimpleTeamSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serialize Teams excluding any information about original activity.
    """

    class Meta:
        model = models.Pair
        fields = 'name', 'students'


class TeamSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serialize Teams excluding any information about original activity.
    """

    class Meta:
        model = models.Pair
        fields = 'name', 'students', 'activity'
