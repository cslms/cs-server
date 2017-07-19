"""
Abstract test cases for activities subclasses and surrounding models.

Subclasses must define a few required models and attributes::

    class Fixtures(ActivityFixtures):
        base_class = MyClass

    class TestMyClass(Fixtures, ActivityTests):
        def test_something(self, activity):
            assert activity.the_answer() == 45

    class TestMySubmissions(Fixtures, SubmissionTests):
        def test_something_else(self, submission):
            assert submission.is_working_well() is True


Classes
-------

.. autoclass:: ActivityFixtures
.. autoclass:: ActivityTests
.. autoclass:: ActivityTestsDb
.. autoclass:: ProgressTests
.. autoclass:: ProgressTestsDb
.. autoclass:: SubmissionTests
.. autoclass:: SubmissionTestsDb
.. autoclass:: FeedbackTests
.. autoclass:: FeedbackTestsDb

"""

import mock
import pytest
from django.core.exceptions import ImproperlyConfigured, ValidationError
from django.db.models import QuerySet
from lazyutils import delegate_to
from mock import patch, Mock

from .mocks import submit_for, queryset_mock, wagtail_page
from ..core.users.factories import UserFactory
from ..core.users.models import User
from ..lms.activities.models import Activity, Progress, Submission, Feedback


#
# Fixtures
#
class ActivityFixtures:
    """
    Expose an "activity" and a "progress" fixtures that do not access the
    database by default.

    Users of this class must define an activity_class class attribute with
    the class that should be tested.
    """

    activity_class = Activity
    submission_payload = {}
    use_db = False

    @pytest.fixture
    def activity(self):
        "An activity instance that does not touch the db."
        return self.activity_class(title='Test', id=1)

    @pytest.fixture
    def activity_db(self):
        "A saved activity instance."
        return self.activity_class(title='Test', id=1)

    @pytest.yield_fixture
    def progress(self, activity, user):
        "A progress instance for some activity."

        cls = self.progress_class

        if cls._meta.abstract:
            pytest.skip('Progress class is abstract')

        with patch.object(cls, 'user', user):
            yield cls(activity_page=activity, id=1)

    @pytest.fixture
    def progress_db(self, progress):
        "A progress instance saved to the db."

        progress.user.save()
        progress.activity.save()
        progress.save()
        return progress

    @pytest.fixture
    def user(self):
        "An user"

        return UserFactory.build(id=2, alias='user')

    # Properties
    progress_class = delegate_to('activity_class')
    submission_class = delegate_to('activity_class')
    feedback_class = delegate_to('activity_class')


# ------------------------------------------------------------------------------
# Activities
#
class ActivityTests(ActivityFixtures):
    """
    Abstract tests for activities.

    You should inherit from this class and maybe write additional tests methods
    for the specific class you want to test.
    """

    # Test valid configuration
    def _check_valid_child_class(self, name, base_class):
        activity_class = self.activity_class
        child_class = getattr(activity_class, '%s_class' % name)
        assert child_class is not None

        if activity_class is not Activity:
            assert child_class is not base_class
            assert activity_class._meta.abstract == child_class._meta.abstract

    def test_activity_has_a_valid_progress_class(self):
        self._check_valid_child_class('progress', Progress)

    def test_activity_has_a_valid_submission_class(self):
        self._check_valid_child_class('submission', Submission)

    def test_activity_has_a_valid_feedback_class(self):
        self._check_valid_child_class('feedback', Feedback)

    # Test error behaviors
    def test_cannot_submit_on_closed_or_disabled_activity(self, activity):
        activity.closed = True
        with pytest.raises(RuntimeError):
            activity.submit(request=Mock())

        activity.closed = False
        activity.disabled = True
        with pytest.raises(RuntimeError):
            activity.submit(request=Mock())

    def test_cannot_submit_if_submission_class_is_not_defined(self, activity):
        activity.submission_class = None

        with pytest.raises(ImproperlyConfigured):
            activity.submit(request=Mock())

    def test_cannot_clean_disabled_activity(self, activity):
        with wagtail_page(self.activity_class):
            activity.disable('error')

        with pytest.raises(ValidationError):
            activity.clean()

    # Test happy stories: user submissions
    def test_submit_payload(self, activity, user, progress):
        request = Mock(user=user)
        for_user = lambda user: progress
        cls = self.activity_class

        with patch.object(cls, 'progress_set', Mock(for_user=for_user)), \
             submit_for(cls):
            sub = activity.submit(request, **self.submission_payload)

        assert isinstance(sub, Submission)
        assert sub.activity is activity

    def test_submit_with_user_kwargs(self, activity):
        request = Mock()
        with patch.object(self.activity_class, 'submit', Mock()) as submit:
            payload = dict(self.submission_payload, probably_invalid_arg=42)
            activity.submit_with_user_payload(request, payload)

        assert submit.call_args == mock.call(
            request, **self.submission_payload)

    def test_submissions_property_yields_a_queryset(self, activity):
        if self.submission_class._meta.abstract:
            return

        with queryset_mock():
            submissions = activity.submissions
            assert isinstance(submissions, QuerySet)

    def test_clean_activity(self, activity):
        activity.owner = User(alias='user', name='John Smith',
                              email='foo@bar.com', school_id='1234')
        activity.clean()
        assert activity.author_name == 'John Smith <foo@bar.com>'


class ActivityTestsDb(ActivityTests):
    """
    Activity tests that requires using the database.
    """
    use_db = True


# ------------------------------------------------------------------------------
# Progress tests
#
class ProgressTests(ActivityFixtures):
    """
    Abstract tests for progress subclasses.
    """

    def test_progress_submission_method(self, activity, progress):
        request = Mock()
        with queryset_mock(), submit_for(self.activity_class):
            sub = submission = progress.submit(
                request, self.submission_payload)

        assert isinstance(sub, Submission)
        assert sub.progress_id == progress.id
        assert sub.activity_id == activity.id


class ProgressTestsDb(ProgressTests):
    """
    Test Progress instances touching the database.
    """

    use_db = True

    def test_recycle_consecutive_submissions(self, db, progress, user):
        request = Mock(user=user)

        with patch.object(self.feedback_class, 'update_autofeedback'):
            sub1 = progress.submit(request, self.submission_payload)
            sub2 = progress.submit(request, self.submission_payload)

        assert sub1.id == sub2.id
        assert sub2.num_recycles == 1


# ------------------------------------------------------------------------------
# Submission tests
#
class SubmissionTests(ActivityFixtures):
    """
    Abstract tests for submission subclasses.
    """

    def test_submission_class_implement_hash(self):
        cls = self.submission_class
        if cls is not Submission:
            assert cls.compute_hash != Submission.compute_hash


class SubmissionTestsDb(SubmissionTests):
    """
    Submissions tests that use the database.
    """
    use_db = True


# ------------------------------------------------------------------------------
# Feedback tests
#
class FeedbackTests(ActivityFixtures):
    """
    Abstract tests for Feedback subclasses.
    """


class FeedbackTestsDb(FeedbackTests):
    """
    Feedback tests that use the database.
    """

    use_db = True
