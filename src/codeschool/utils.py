import hashlib
from functools import lru_cache

from django.db.models import QuerySet, Model, Manager
from django.db.models.manager import BaseManager
from lazyutils import delegate_to, lazy
from ipware.ip import get_real_ip, get_ip as _get_ip


class delegate_to_or_none(delegate_to):
    """
    Like delegate_to(), but return None if delegate is None.
    """

    def __get__(self, obj, cls=None):
        if obj is None:
            return self
        owner = getattr(obj, self.attribute)
        if owner is None:
            return None
        try:
            attr = self._name
        except AttributeError:
            attr = self._name = self._get_name(cls)
        return getattr(owner, attr)


def indent(text, prefix=4):
    """
    Indent string of text.
    """

    if isinstance(prefix, int):
        prefix = ' ' * prefix
    return '\n'.join(prefix + line for line in text.splitlines())


def manager_class(model, queryset_class=None, class_name=None,
                  use_for_related_fields=False):
    """
    Return the manager class for model.

    If an optional queryset is given, returns a new class using the
    Manager.from_queryset() API.
    """

    for cls in model.mro():
        if not issubclass(model, Model):
            continue
        try:
            mgm = cls.objects
            break
        except AttributeError:
            pass
    else:
        mgm = Manager()

    if not isinstance(mgm, BaseManager):
        raise TypeError('unexpected manager class: %s' %
                        mgm.__class__.__name__)

    if queryset_class is not None:
        mgm = mgm.from_queryset(queryset_class, class_name=class_name)

    if use_for_related_fields:
        mgm.use_for_related_fields = True

    return mgm


def manager_instance(model, queryset_class=None, class_name=None, **kwargs):
    """
    Like manager_class, but return a manager instance.
    """

    return manager_class(model, queryset_class, class_name, **kwargs)()


def queryset_class(model):
    """
    Return the queryset class for model.
    """

    mgm = manager_class(model)

    # Assume manager was created using Manager.from_queryset(qs)
    try:
        qs_class = mgm._queryset_class
        if not issubclass(qs_class, QuerySet):
            name = qs_class.__class__.__name__
            raise TypeError('unexpected manager class: %s' % name)
        return qs_class
    except AttributeError:
        raise ValueError('could not determine queryset class')


def exception_to_json(ex):
    """
    JSON compatible representation of an exception.
    """

    return {
        'exception': ex.__class__.__name__,
        'message': ex.args,
    }


class LazyManager:
    """
    Lazy accessor for a Model's manager.
    """

    @lazy
    def model(self):
        from django.apps import apps
        return apps.get_model(self._app, self._model)

    @lazy
    def _manager(self):
        return getattr(self.model, self._manager_attr)

    def __init__(self, app, model, manager='objects'):
        self._app = app
        self._model = model
        self._manager_attr = manager

    def __getattr__(self, attr):
        return getattr(self._manager, attr)


@lru_cache(1024)
def md5hash(st):
    """
    Compute the hex-md5 hash of string.

    Returns a string of 32 ascii characters.
    """

    return hashlib.md5(st.encode('utf8')).hexdigest()


def md5hash_seq(seq):
    """
    Combined md5hash for a sequence of string parameters.
    """

    hashes = [md5hash(x) for x in seq]
    return md5hash(''.join(hashes))


def get_ip(request):
    """
    Return the best possible inference for the user's ip adress from a request.
    """

    return get_real_ip(request) or _get_ip(request) or ''
