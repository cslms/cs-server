import pytest

from mock import patch, Mock
from codeschool.models import User
from codeschool.lms.activities.tests.mocks import wagtail_page
from codeschool.sparta.models import SpartaActivity, UserGrade
from codeschool.sparta.models.activity import read_csv_file


class TestActivity:
    activity_class = SpartaActivity
    submission_payload = {}

    @pytest.fixture
    def activity(self):
        cls = self.activity_class
        with wagtail_page(cls):
            result = cls(title='Test', id=1)
        result.specific = result
        return result

    # Mocked fixtures
    user = pytest.fixture(lambda self: Mock(id=2, username='user'))

    def test_read_csv(self):
        data = read_csv_file('a;1\nb;2')
        assert data[0] == ('a', 1.0)

    def test_create_user_grades(self, activity: SpartaActivity):
        csv_data = 'a;1\nb;2'
        users = [User(username='a'), User(username='b')]

        def patched(**kwargs):
            return users

        with patch.object(User.objects, 'filter', patched):
            print(activity, type(activity))
            objs = activity.populate_from_csv(csv_data, commit=False)

        assert len(objs) == 2
        grade1, grade2 = objs
        assert grade1.grade == 1.0