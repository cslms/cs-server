import pytest
from lazyutils import delegate_to
from mock import patch, Mock

from codeschool.accounts.factories import UserFactory
from codeschool.lms.activities.models import Activity
from codeschool.lms.activities.tests.mocks import wagtail_page


class Fixtures:
    activity_class = Activity
    submission_payload = {}

    @pytest.fixture
    def activity(self):
        cls = self.activity_class
        with wagtail_page(cls):
            result = cls(title='Test', id=1)
        result.specific = result
        return result

    @pytest.yield_fixture
    def progress(self, activity, user):
        cls = self.progress_class
        if cls._meta.abstract:
            pytest.skip('Progress class is abstract')

        with patch.object(cls, 'user', user):
            progress = cls(activity_page=activity, id=1)
            yield progress

    # Mocked fixtures
    user = pytest.fixture(lambda self: Mock(id=2, username='user'))

    # Properties
    progress_class = delegate_to('activity_class')
    submission_class = delegate_to('activity_class')
    feedback_class = delegate_to('activity_class')


class DbFixtures(Fixtures):
    @pytest.fixture
    def activity(self):
        result = self.activity_class(title='Test', id=1)
        result.specific = result
        return result

    @pytest.fixture
    def progress(self, activity, user):
        cls = self.progress_class
        if cls._meta.abstract:
            pytest.skip('Progress class is abstract')
        return cls(activity_page=activity, user=user, id=1)

    @pytest.fixture
    def progress_db(self, progress):
        progress.user.save()
        progress.activity.save()
        progress.save()
        return progress

    @pytest.fixture
    def user(self):
        return UserFactory.build()
