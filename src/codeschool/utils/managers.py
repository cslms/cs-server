from django.db.models import Model, Manager, QuerySet
from django.db.models.manager import BaseManager
from lazyutils import lazy


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
