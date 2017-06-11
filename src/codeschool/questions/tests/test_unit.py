import pytest
from mock import Mock

from codeschool.tests import ActivityTests
from codeschool.questions.models import Question


class TestQuestions(ActivityTests):
    """
    Test abstract questions.
    """

    activity_class = Question

    @pytest.fixture
    def question(self, activity):
        return activity

    def test_filter_submission_kwargs_for_ajax_submission(self, question):
        data = dict(self.submission_payload, very_unlikely_kwarg=42)
        kwds = question.filter_user_submission_payload(Mock(), data)
        assert 'very_unlikely_kwarg' not in kwds
        assert kwds == self.submission_payload
