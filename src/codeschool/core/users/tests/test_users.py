import pytest

from codeschool.core.users.factories import (
    FullUserFactory, UserFactory,
    make_yoda_teacher, make_teachers, make_students
)

pytestmark = pytest.mark.db


class TestUser:
    def test_user_has_profile(self):
        user = UserFactory.build()
        assert user.profile.user is user


class TestUserFactories:
    def test_create_yoda(self):
        yoda = make_yoda_teacher(commit=False)
        assert yoda.profile
        assert yoda.profile.age == 900

    def test_create_teachers(self):
        teachers = make_teachers(commit=False)
        assert len(teachers) == 4
        assert all(x.role == x.ROLE_TEACHER for x in teachers)

    def test_create_students(self):
        students = make_students(5, commit=False)
        assert len(students) == 5
        assert all(x.role == x.ROLE_STUDENT for x in students)


@pytest.mark.django_db
class TestUserDb:
    def test_user_profile_is_created_automatically(self):
        user = FullUserFactory.create()
        assert user.profile is not None
