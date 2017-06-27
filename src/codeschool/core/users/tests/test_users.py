import pytest

from codeschool.core.users.factories import FullUserFactory, UserFactory

pytestmark = pytest.mark.db


class TestUser:
    def test_user_has_profile(self):
        user = UserFactory.build()
        assert user.profile.user is user


@pytest.mark.django_db
class TestUserDb:
    def test_user_profile_is_created_automatically(self):
        user = FullUserFactory.create()
        assert user.profile is not None
