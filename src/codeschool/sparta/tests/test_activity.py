import pytest

from mock import patch, Mock, MagicMock, mock
from codeschool.models import User
from types import SimpleNamespace
from codeschool.sparta.models import SpartaActivity, UserGrade
from codeschool.sparta.models.activity import read_csv_file


class TestActivity:
    activity_class = SpartaActivity
    submission_payload = {}

    @pytest.fixture
    def activity(self):
        cls = self.activity_class
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

    def test_create_post_grade_csv(self, activity: SpartaActivity):
        csv_data_should_be = 'a;1\nb;4\nc;5\n'

        with patch.object(UserGrade, 'user', None):
            users = [
                Mock(spec=User, id=1, username='a'),
                Mock(spec=User, id=2, username='b'),
                Mock(spec=User, id=3, username='c')
            ]

            users_grade = [
                UserGrade(user=users[0], grade=1, activity=activity),
                UserGrade(user=users[1], grade=2, post_grade=4, activity=activity),
                UserGrade(user=users[2], grade=3, post_grade=5, activity=activity)
            ]


            ns = SimpleNamespace(all=lambda: users_grade, select_related=lambda self: ns)

            with patch.object(SpartaActivity, 'user_grades', ns):
                csv = activity.create_post_grade_csv()

                assert csv == csv_data_should_be
