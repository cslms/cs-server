from rest_framework import serializers

from codeschool.questions.base import models


class QuestionSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serialize questions.
    """

    class Meta:
        model = models.Question
        fields = 'title', 'short_description', 'body', 'comments', \
                 'author_name', 'visible', 'closed', 'max_group_size',
