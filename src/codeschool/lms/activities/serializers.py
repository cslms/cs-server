from rest_framework.serializers import ModelSerializer

from . import models


class ActivitySerializer(ModelSerializer):
    class Meta:
        model = models.Activity
        fields = ('id', 'title', 'author_name', 'visible', 'closed')


class ProgressSerializer(ModelSerializer):
    class Meta:
        model = models.Progress
        fields = ('user', 'activity_page', 'final_grade_pc',
                  'given_grade_pc', 'finished', 'best_submission')


class SubmissionSerializer(ModelSerializer):
    class Meta:
        model = models.Submission
        fields = ('progress', 'hash')


class FeedbackSerializer(ModelSerializer):
    class Meta:
        model = models.Feedback
        fields = ()
