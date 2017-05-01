from collections import OrderedDict
from contextlib import contextmanager
from types import SimpleNamespace, MethodType

from django.db.models import QuerySet
from django.db.models.query import ModelIterable
from lazyutils import lazy
from mock import patch


class Model(SimpleNamespace):
    """
    A mock model object.

    This is much faster than Django's standard constructors. All attributes are
    set to None.
    """

    id = None
    LAST_ID = 0

    @classmethod
    def create(cls, **kwargs):
        """
        Creates a new instance.
        """

        new = cls(**kwargs)
        if new.id is None:
            Model.LAST_ID += 1
            new.id = Model.LAST_ID
        return new

    def __getattr__(self, attr):
        try:
            return super().__getattr__(attr)
        except AttributeError:
            return None


class Db:
    """
    A container that mocks a database.

    It is implemented internally as a dictionary from pk's to objects.
    """

    def __init__(self, data=()):
        self._data = OrderedDict()
        for elem in data:
            self._data[elem.id] = elem
        self._data.pop(None, None)

    def __iter__(self):
        return iter(self._data.values())

    def __repr__(self):
        sorted_items = sorted(self._data.items(), key=lambda x: x[0])
        lines = ['%s: %s' % item for item in sorted_items]
        return '\n'.join(lines)

    def save(self, obj, *args, **kwargs):
        """
        Saves object on fake database.
        """

        if obj.id is None:
            obj.id = max(self._data or (0,)) + 1
        self._data[obj.id] = obj
        print(self._data)


class FakeQuerySet(QuerySet):
    @lazy
    def _result_cache(self):
        return list(self._data)

    def __init__(self, model=None, query=None, using=None, hints=None,
                 data=None, mirror=None):
        super().__init__(model, query, using, hints)
        self._data = Db() if data is None else data
        self._mirror = mirror
        del self._result_cache

        # Changes the iterable class to iterate using the fake db
        if self._iterable_class is ModelIterable:
            self._iterable_class = lambda self: iter(self._data)

    def _wrapped_method(self, func):
        def wrapped(*args, **kwargs):
            result = func(*args, **kwargs)
            if isinstance(result, QuerySet):
                result = FakeQuerySet(self.db, QuerySet)
            return result

    def __getattr__(self, attr):
        obj = getattr(self._mirror, attr)
        if hasattr(obj, '__func__'):
            return MethodType(obj.__func__, self)
        return obj

    def iterator(self):
        return iter(self._data)

    __iter__ = iterator

    def __len__(self):
        return len(self._data)

@contextmanager
def mock_manager(manager, data=None, save=False):
    """
    Mocks a manager to return FakeQuerySets instead of regular querysets.

    Args:
        manager:
            A manager object
        data:
            Initial data in the fake database.
        save:
            If True, mocks the .save() method of models.
    """

    data = Db() if data is None else data

    old_getter = manager.get_queryset

    def get_queryset():
        queryset = old_getter()
        return FakeQuerySet(model=manager.model, using=manager._db,
                            hints=manager._hints, data=data, mirror=queryset)

    def save(self, *args, **kwargs):
        print('saving', self)
        return data.save(self, *args, **kwargs)

    model = manager.model

    with patch.object(manager, 'get_queryset', get_queryset):
        try:
            if save:
                model.__save = model.save
                model.save = save
            yield data

        finally:
            if save:
                model.save = model.__save
