from rest_framework import serializers

from . import models


class ClassroomSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serialize Classroom objects.
    """

    class Meta:
        model = models.Classroom
        fields = (
            'url', 'name', 'slug', 'discipline', 'course', 'teacher',
            'short_description', 'description',
            'students', 'staff', 'weekly_lessons',
            'subscription_passphrase',
            'accept_subscriptions', 'is_public',
        )
