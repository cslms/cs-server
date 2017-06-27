import pytest


@pytest.mark.skip('wait for urlchecker')
class TestUrls:
    def test_basic_urls(self, user, client):
        context = {'username': user.username}
        urls = [
            '/auth/{username}',
            '/auth/{username}/edit',
            '/auth/{username}/password',
        ]
        client.check_url(urls, context, html5=True)

    @pytest.mark.django_db
    def test_non_authenticaded_auth_urls(self, urlchecker):
        urlchecker.check_ok(
            [
                '/auth/login/',
            ],
            html5=True,
        )

    @pytest.mark.django_db
    def test_authenticated_auth_urls(self, urlchecker, user_with_profile):
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


