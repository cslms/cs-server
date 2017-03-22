import functools
import traceback
from functools import partial
from io import StringIO

from django.contrib.auth import authenticate

from codeschool import models
from codeschool.questions.coding_io.loaders import load_markio


RESOURCE_TYPE_EQUIVALENCES = {
    'markio': 'coding_io/markio',
}


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
    if not (user.is_superuser or parent_page.owner == user):
        path = parent_page.url_path.partition('/')[2]
        raise JSONEncodedError({
            'error': 'permission',
            'message': 'you don\'t have permissions to write under %s' % path
        })


def normalize_resource_type(resource_type):
    """
    Normalizes the resource_type string.
    """

    name = resource_type.casefold()
    return RESOURCE_TYPE_EQUIVALENCES.get(name, name)


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


def wrap_json_rpc(function):
    """
    Wraps function to with a JSON-RPC friendly way of handling exceptions.
    """

    def convert(x):
        if isinstance(x, bytes):
            return x.decode('utf8')
        return x

    @functools.wraps(function)
    def decorated(*args, **kwargs):
        args = tuple(convert(x) for x in args)
        kwargs = {k: convert(v) for k, v in kwargs.items()}

        try:
            result = function(*args, **kwargs)
        except Exception as ex:
            if isinstance(ex, JSONEncodedError):
                data = ex.data
                data.setdefault('error', 'RPCError')
            else:
                data = {'error': 'runtime', 'message': str(ex)}
            tb = ex.__traceback__
            file = StringIO()
            traceback.print_tb(tb, file=file)
            data['traceback'] = file.getvalue()
            return data
        return result

    return decorated


def resource_to_url(function):
    """
    Decorates function to return a dictionary with the resource url.

    If the return value of function is ``obj``, this decorator transforms it to

    ::

        {'url': obj.get_absolute_url(), 'status': 'success'}
    """

    @functools.wraps(function)
    def decorated(*args, **kwargs):
        result = function(*args, **kwargs)
        return {'url': result.get_absolute_url(), 'status': 'success'}

    return decorated
