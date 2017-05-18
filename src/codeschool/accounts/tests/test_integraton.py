import pytest

from codeschool.accounts.factories import FullUserFactory

pytestmark = pytest.mark.integration

@pytest.mark.django_db
def test_user_profile_is_created_automatically():
    user = FullUserFactory.create()
    assert user.profile is not None
