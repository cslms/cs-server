from contextlib import contextmanager

from django.db.models import QuerySet
from mock import patch

from codeschool.lms.activities.models.mixins import CommitMixin


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

    with patch.object(cls, 'specific', specific) as patcher:
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

    progress_class = cls.progress_class
    with wagtail_page(cls) as patcher:
        with patch.object(cls.submission_class.objects,
                          'recyclable',
                          lambda x: []):
            with patch.object(cls.submission_class, 'full_clean'):
                yield patcher


@contextmanager
def queryset_mock(data=(), cls=QuerySet):
    """
    Mocks a few methods in the queryset API to make them return mocks instead
    of consulting the database.
    """

    forbidden = {'__module__', '__name__',
                 '__dict__', '__doc__', '__weakref__'}

    # We abuse the "class" sugar and make it return the namespace dictionary
    # instead of creating a regular type
    class Namespace:

        def __new__(cls, name, bases, ns):
            return ns

    class methods(metaclass=Namespace):
        """
        This is a namespace of methods.
        """

        _data = list(data)

        def __len__(self):
            return len(self._data)

    del methods['__module__']
    del methods['__qualname__']
    del methods['__doc__']

    # Patch QuerySet and later undo all modifications
    old = {k: getattr(cls, k) for k in methods if hasattr(cls, k)}
    try:
        for attr, method in methods.items():
            setattr(cls, attr, method)
        yield
    finally:
        for attr in methods:
            try:
                setattr(cls, attr, old[attr])
            except KeyError:
                delattr(cls, attr)
