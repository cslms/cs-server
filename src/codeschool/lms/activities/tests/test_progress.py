from mock import Mock, patch

from codeschool.lms.activities.models import Submission
from codeschool.lms.activities.tests.fixtures import Fixtures, DbFixtures
from codeschool.lms.activities.tests.mocks import queryset_mock, submit_for


class TestSubmission(Fixtures):
    def test_submission_class_implement_hash(self):
        cls = self.submission_class
        if cls is not Submission:
            assert cls.compute_hash != Submission.compute_hash


class TestProgress(Fixtures):
    def test_progress_submission_method(self, activity, progress):
        request = Mock()
        with queryset_mock(), submit_for(self.activity_class):
            sub = submission = progress.submit(request, self.submission_payload)

        assert isinstance(sub, Submission)
        assert sub.progress_id == progress.id
        assert sub.activity_id == activity.id


class DbTestProgress(DbFixtures):
    def test_recycle_consecutive_submissions(self, db, progress, user):
        request = Mock(user=user)

        with patch.object(self.feedback_class, 'update_autofeedback'):
            sub1 = progress.submit(request, self.submission_payload)
            sub2 = progress.submit(request, self.submission_payload)

        assert sub1.id == sub2.id
        assert sub2.num_recycles == 1
