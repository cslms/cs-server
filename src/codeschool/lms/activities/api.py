from rest_framework import viewsets

from . import models
from . import serializers


# class ActivityViewSet(viewsets.ModelViewSet):
#     queryset = models.Activity.objects.all()
#     serializer_class = serializers.ActivitySerializer


class ProgressViewSet(viewsets.ModelViewSet):
    queryset = models.Progress.objects.all()
    serializer_class = serializers.ProgressSerializer


class SubmissionViewSet(viewsets.ModelViewSet):
    queryset = models.Submission.objects.all()
    serializer_class = serializers.SubmissionSerializer


class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = models.Feedback.objects.all()
    serializer_class = serializers.FeedbackSerializer


def register(router, prefix=''):
    # router.register(prefix + 'activities', ActivityViewSet)
    router.register(prefix + 'progress', ProgressViewSet)
    router.register(prefix + 'submissions', SubmissionViewSet)
    router.register(prefix + 'feedbacks', FeedbackViewSet)