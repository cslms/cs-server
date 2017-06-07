import pytest

def _test_basic_urls(user, client):
    context = {'username': user.username}
    urls = [
        '/auth/{username}',
        '/auth/{username}/edit',
        '/auth/{username}/password',
    ]
    client.check_url(urls, context, html5=True)


def _test_login_with_valid_user(driver, user_with_password, password):
    user = user_with_password
    driver.open('/')

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
