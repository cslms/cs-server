from contextlib import contextmanager

from django.db.models import QuerySet
from mock import patch

from ..mixins import CommitMixin

# Make static analyzers happy :)
patch_object = getattr(patch, 'object')


@contextmanager
def disable_commit():
    """
    Disable commits for CommitMixin subclasses.
    """
    try:
        CommitMixin.DISABLE_COMMIT = True
        yield
    finally:
        CommitMixin.DISABLE_COMMIT = False


@contextmanager
def wagtail_page(cls):
    """
    A context manager that can be used to make wagtail pages usable without
    using the database.

    Args:
        cls: The model for the wagtail page.

    Examples:

        with wagtail_page(MyPage):
            page = MyPage(title=1,2,3)
    """
    specific = property(lambda self: self)

    with patch_object(cls, 'specific', specific) as patcher:
        try:
            CommitMixin.DISABLE_COMMIT = True
            yield patcher
        finally:
            CommitMixin.DISABLE_COMMIT = False


@contextmanager
def submit_for(cls):
    """
    Makes submission work without access to the database.
    """

    with wagtail_page(cls) as patcher:
        with patch_object(cls.submission_class.objects,
                          'recyclable',
                          lambda x: []):
            with patch_object(cls.submission_class, 'full_clean'):
                yield patcher


@contextmanager
def queryset_mock(data=(), cls=QuerySet):
    """
    Mocks a few methods in the queryset API to make them return mocks instead
    of consulting the database.
    """

    # We abuse the "class" sugar and make it return the namespace dictionary
    # instead of creating a regular type
    class Namespace:
        def __new__(cls, name, bases, ns):
            return ns

    class Methods(metaclass=Namespace):
        """
        This is a namespace of methods.
        """

        _data = list(data)

        def __len__(self):
            return len(self._data)

    del Methods['__module__']
    del Methods['__qualname__']
    del Methods['__doc__']

    # Patch QuerySet and later undo all modifications
    old = {k: getattr(cls, k) for k in Methods if hasattr(cls, k)}
    try:
        for attr, method in Methods.items():
            setattr(cls, attr, method)
        yield
    finally:
        for attr in Methods:
            try:
                setattr(cls, attr, old[attr])
            except KeyError:
                delattr(cls, attr)
