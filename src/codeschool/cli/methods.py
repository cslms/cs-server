from functools import partial

from django.contrib.auth import authenticate

from codeschool import models
from codeschool.questions.coding_io.utils import load_markio
from . import api


class JSONEncodedError(Exception):
    """
    An error that can be encoded in JSON and should be the return value for an
    RPC method failure mode.
    """

    @property
    def data(self):
        return self.args[0]


def get_parent_from_hint(parent):
    """
    Return the parent page from the given parent page hint.
    """

    parent = parent if parent.endswith('/') else parent + '/'
    pages = models.Page.objects.filter(url_path__endswith=parent)
    print(pages)
    return pages.get()


def validate_user(username, password):
    """
    Return valid user or raise JSONEncodedError({'error': 'auth', ...})
    """

    user = authenticate(username=username, password=password)
    if user is None:
        raise JSONEncodedError({
            'error': 'auth',
            'message': 'Invalid username/password.',
        })
    return user


def check_write_permissions(user, parent_page):
    """
    Raise an JSONEncodedError if user does not have permission to write a child
    page under the given parent page.
    """
    if not user.is_superuser:
        path = parent_page.url_path.partition('/')[2]
        raise JSONEncodedError({
            'error': 'permission',
            'message': 'you don\'t have permissions to write under %s' % path
        })


def normalize_resource_type(resource_type):
    """
    Normalizes the resource_type string.
    """

    return resource_type.casefold()


def get_loader(resource_type):
    """
    Return the loader function for the given resource type.

    A loader function simply takes a data string and returns the corresponding
    resource.
    """

    if resource_type == 'coding_io/markio':
        return partial(load_markio, update=True)
    else:
        raise JSONEncodedError({
            'error': 'resource_type',
            'message': 'unknown resource type: %r' % resource_type
        })


def push_resource_worker(data, resource_type, parent, auth):
    """
    Put or update resource to Codeschool.

    Args:
        data:
            Resource contents. Must be a string of data. Binary contents should
            be Base64 encoded.
        resource_type:
            Resource type.
        parent:
            A hint to the parent page for the resource.
        auth:
            Authentication credentials (username, password).

    Returns:
        A JSON encoded message.
    """

    user = validate_user(*auth)
    parent = get_parent_from_hint(parent)
    check_write_permissions(user, parent)
    resource_type = normalize_resource_type(resource_type)

    # Load
    loader = get_loader(resource_type)
    try:
        result = loader(data, parent)
    except (SyntaxError, ValueError) as ex:
        return {
            'error': 'resource',
            'type': resource_type,
            'message': str(ex)
        }

    return {
        'url': result.get_absolute_url(),
        'status': 'success',
    }


@api.dispatcher.add_method
def push_resource(data, resource_type, parent, auth):
    """
    API entry point with a JSON-RPC friendly handling of exceptions.
    """

    try:
        return push_resource_worker(data, resource_type, parent, auth)
    except JSONEncodedError:
        return JSONEncodedError.data
