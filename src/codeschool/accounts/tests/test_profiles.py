import pytest

from codeschool.accounts.factories import *


@pytest.mark.django_db
def test_user_profile_is_created_automatically():
    user = FullUserFactory.create()
    assert user.profile is not None


@pytest.mark.skip('wait for urlchecker')
@pytest.mark.django_db
def test_non_authenticaded_auth_urls(urlchecker):
    urlchecker.check_ok(
        [
            '/auth/login/',
        ],
        html5=True,
    )


@pytest.mark.skip('wait for urlchecker')
@pytest.mark.django_db
def test_authenticated_auth_urls(urlchecker, user_with_profile):
    user = user_with_profile
    urlchecker.check_ok(
        [
            '/auth/{user.username}/',
            '/auth/{user.username}/edit/',
            '/auth/{user.username}/password/',
            '/auth/{user.username}/logout/',
            '/auth/',
        ],
        url_data={'user': user},
        html5=False,
        login=user,
    )
