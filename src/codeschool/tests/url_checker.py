import pytest


def pytest_generate_tests(metafunc):
    """This function is called to generate tests for URLBaseTester subclasses.
    It creates a new test case for each registered URL.

    It should be imported in the test module to make effect.
    """
    cls = metafunc.cls
    if cls is not URLBaseTester and isinstance(cls, type) and \
            issubclass(cls, URLBaseTester):
        if 'public_url' in metafunc.fixturenames:
            metafunc.parametrize('public_url', metafunc.cls.public_urls)
        if 'login_url' in metafunc.fixturenames:
            metafunc.parametrize('login_url', metafunc.cls.login_urls)
        if 'private_url' in metafunc.fixturenames:
            metafunc.parametrize('private_url', metafunc.cls.private_urls)


class URLBaseTester:
    """
    Subclass this class naming it TestURLs or something similar and define the
    public_urls, login_urls and private_urls sequences.
    """
    public_urls = []
    login_urls = []
    private_urls = []

    def expect(self, a, b, response, url):
        try:
            assert a <= response.status_code < b
        except AssertionError:
            print('HEADERS')
            for k, v in response.items():
                print('    %s: %s' % (k, v))
            print('URL\n    %s' % url)
            print('RESPONSE\n    %r' % response)
            if response.status_code not in [404, 500]:
                print('BODY')
                data = (response.content.decode('utf8') or '<empty>')
                for line in data.splitlines():
                    print('    ' + line)
                raise

    @pytest.mark.django_db
    def test_public_url_accessible(self, client, public_url):
        response = client.get(public_url, follow=True)
        self.expect(200, 300, response, public_url)

    @pytest.mark.django_db
    def test_login_url_hidden_from_anonymous(self, client, login_url):
        response = client.get(login_url, follow=True)
        self.expect(400, 500, response, login_url)

    @pytest.mark.django_db
    def test_login_url_accessible(self, client, user, login_url):
        client.force_login(user)
        response = client.get(login_url, follow=True)
        self.expect(400, 500, response, login_url)

    @pytest.mark.django_db
    def test_private_urls_hidden_from_regular_users(self, client, user, private_url):
        response = client.get(private_url, follow=True)
        self.expect(400, 500, response, private_url)

    @pytest.mark.django_db
    def test_private_urls_visible_to_owner(self, client, user, private_user, private_url):
        client.force_login(private_user)
        response = client.get(private_url, follow=True)
        self.expect(400, 500, response, private_url)