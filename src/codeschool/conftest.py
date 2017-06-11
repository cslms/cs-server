"""
Functions and fixtures that aids writing unit tests.
"""

import pytest
from mommys_boy import mommy, fake

from codeschool.accounts.factories import UserFactory, FullUserFactory, birthday
from sulfur import Driver as _SulfurDriver
from sulfur.django import client

# Helper functions
mommy_make = mommy.make
mommy_create = mommy.create
mommy_factory = mommy.get_factory

# Set up sulfur to use django
client = pytest.fixture(client)


def model_fixture(func):
    """
    Marks function that returns a Model instance as a fixture

    Consider the example::

        @model_fixture
        def foo():
            return ...

    This is the same as::

        @pytest.fixture
        @pytest.mark.db
        def foo():
            return ...
    """
    return pytest.fixture(pytest.mark.db(func))


# Fixtures
@pytest.fixture
def base_page_location_kwargs():
    """Define a proper location for the given page in wagtail's tree."""

    return {
        'path': '1234',
        'depth': 1,
        'numchild': 0,
    }


@pytest.fixture
def sulfur_wait():
    """
    The value that will be passed to the implicit wait parameter in selenium.
    """

    return 1


@pytest.fixture
def ui(selenium, live_server, sulfur_wait):
    """
    Return a initialized sulfur driver instance.

    The sulfur driver wraps selenium in a more convenient interface.
    """

    return _SulfurDriver(selenium, base_url=live_server.url, wait=sulfur_wait)


@pytest.fixture
def html(ui):
    """The dom attribute of a driver ui.

    It can be used to access elements in the page with defined ids. It is also
    useful for filling up forms as in the example::

        ... (open page)
        html.formButton.click()      # clicks the button with id="formButton"
        html.id_name = 'John'        # send the keys 'John' to the form element
        html['send-button'].click()  # alternative API for element whose id's are
                                     # not valid python names.
    """

    return ui.ids


@pytest.fixture
def soup(ui):
    """
    Beautiful soup accessor.
    """

    raise NotImplementedError


@pytest.fixture
def url_data(url_owner):
    return None


@pytest.fixture
def url_owner(user):
    return user


@pytest.fixture
def public_url(request):
    return request.param


@pytest.fixture
def login_url(request, user):
    return request.param.format(user=user)


@pytest.fixture
def password():
    """A random password."""

    return fake.password()


@pytest.fixture
def user(db):
    """
    A simple user account (no valid password).

    Pre and post save signals are disabled.
    """

    return UserFactory.create()


@pytest.fixture
def user_with_profile(db):
    """
    User account with a profile.
    """

    return FullUserFactory.create()


@pytest.fixture
def user_with_password(db, password):
    """
    User account with password (use together with the password fixture).
    """

    user = UserFactory.create()
    user.set_password(password)
    user.save()
    return user


@pytest.fixture
def request_with_user(rf, user):
    request = rf.get('/')
    request.user = user
    return request


birthday = pytest.fixture(birthday)
