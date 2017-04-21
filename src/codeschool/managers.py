import inspect

from django.core.exceptions import ImproperlyConfigured
from django.db import models
from django.db.models.fields.related_descriptors import \
    ReverseManyToOneDescriptor
from lazyutils import lazy


def apply_manager_extensions(*args):
    """
    Apply extensions to manager.

    Extension methods of the form ``<manager>__<name>(queryset|manager, *args)``
    in a Model subclass are applied to the associated manager object.

    You can use the regular API::

        apply_manager_extensions(cls, name):
            Apply all extensions to the given name. Return none.

    Or the decorator form::

        @apply_manager_extensions('objects')
        class MyModel(Model):
            def objects__today(queryset):
                today = timezone.now().date
                return queryset.filter(date=today)
    """

    if len(args) == 1:
        def decorator(cls):
            apply_manager_extensions(cls, *args)
            return cls

    # Find extensions and classify as queryset or manager extensions
    cls, manager_name = args
    queryset_exts, manager_exts = _ext_methods(*args, remove_extensions=True)

    # Create a new manager class
    queryset_class = None
    manager_obj = getattr(cls, manager_name)
    queryset_name = '%sQuerySet' % cls.__name__
    manager_class_name = '%sManager' % cls.__name__

    # We get the queryset object and change its __class__ attribute to the
    # correct subclass.
    def get_queryset(self):
        nonlocal queryset_class

        qs = super().get_queryset()
        if queryset_class is None:
            qsclass = type(qs)
            queryset_class = type(queryset_name, (qsclass,), queryset_exts)
        qs.__class__ = queryset_class
        manager_obj._has_extensions = True
        return qs

    # A similar approach here: change the manager object class
    manager_exts['get_queryset'] = get_queryset
    manager_class = type(manager_class_name,
                         (type(manager_obj),), manager_exts)
    manager_obj.__class__ = manager_class
    manager_obj._has_extensions = True


def _ext_methods(cls, manager_name, remove_extensions=False):
    """
    Return a tuple with (queryset_methods, manager_methods) dictionaries.

    If ``remove_extensions=True``, delete all extension methods from the model
    class `cls`.
    """

    prefix = manager_name + '__'
    prefix_size = len(prefix)
    queryset_exts = {}
    manager_exts = {}
    all_exts = [x for x in dir(cls) if x.startswith(prefix)]
    for ext in all_exts:
        func = getattr(cls, ext)
        argspec = inspect.getargspec(func)
        funcname = ext[prefix_size:]
        func.__name__ = funcname
        if remove_extensions:
            type(cls).__delattr__(cls, ext)
        if argspec.args[0] in ['qs', 'queryset']:
            queryset_exts[funcname] = func
            manager_exts[funcname] = _manager_from_qs(funcname, func)
        elif argspec.args[0] in ['mgm', 'manager']:
            manager_exts[funcname] = func
        else:
            raise ImproperlyConfigured(
                'Manager extension methods must start with either with a '
                '"queryset" or "manager" argument.'
            )
    return queryset_exts, manager_exts


def _manager_from_qs(name, func):
    """
    Return a manager method from a queryset method.
    """

    def method(self, *args, **kwargs):
        qs = self.get_queryset()
        func = getattr(qs, name)
        return func(*args, **kwargs)
    method.__name__ = name
    method.__doc__ = func.__doc__
    return method


def discover_manager_extensions(cls):
    """
    Return a list with all manager names that define extension methods.
    """

    return ['objects']


def auto_manager_extensions(cls):
    """
    Decorator that discovers and applies all manager extensions.
    """

    managers = discover_manager_extensions(cls)
    for manager in managers:
        apply_manager_extensions(cls, manager)
    return cls


class DiscoverableManagerMeta(type(models.Model)):
    """
    Metaclass that automatically discover manager extensions.
    """

    def __init__(self, name, bases, ns):
        super().__init__(name, bases, ns)

        try:
            DiscoverableManagerModel
        except NameError:
            pass
        else:
            auto_manager_extensions(self)


class DiscoverableManagerModel(type(models.Model),
                               metaclass=DiscoverableManagerMeta):
    """
    Model base class that automatically discover manager extensions.
    """


class ExtensibleManagerDescriptor:
    """
    A descriptor that implements an extensible manager.
    """

    def __init__(self, cls, name):
        self._cls = cls
        self._name = name
        self._descriptor = cls.__dict__[name]

    def __get__(self, obj, cls=None):
        result = self._descriptor.__get__(obj, cls)
        if obj is not None:
            if not getattr(result, '_has_extensions', False):
                apply_manager_extensions(self._cls, self._name)
        return result

    def __set__(self, obj, value):
        self._descriptor.__set__(obj, value)


#
# Related managers
#
class RelatedDescriptorExt(ReverseManyToOneDescriptor):
    """
    A descriptor that automatically extends the default related manager
    descriptor by inserting the given ext_class in the mro().
    """

    def __init__(self, descriptor, ext_class):
        super().__init__(descriptor.rel)
        self.descriptor = descriptor
        self.ext_class = ext_class

    @lazy
    def ext_class_final(self):
        # We test these two attributes in order to support ModelCluster
        # descriptors and the vanilla Django ones.
        for attr in ('child_object_manager_cls', 'related_manager_cls'):
            try:
                manager_cls = getattr(self.descriptor, attr)
            except AttributeError:
                continue
            else:
                class DescriptorExt(self.ext_class, manager_cls):

                    def __new__(cls, *args, **kwargs):
                        return manager_cls.__new__(cls, *args, **kwargs)

                    def __init__(self, *args, **kwargs):
                        manager_cls.__init__(self, *args, **kwargs)

                    def __get__(self, instance, cls=None):
                        return manager_cls.__get__(instance, cls=cls)

                    def __getattr__(self, attr):
                        return getattr(manager_cls, attr)

                return DescriptorExt

        raise RuntimeError('could not determine the manager class from the'
                           'descriptor: %r' % self.descriptor)

    def __get__(self, instance, cls=None):
        if instance is None:
            return self
        return self.ext_class_final(instance)

    def __set__(self, instance, value):
        self.descriptor.__set__(instance, value)


class RelatedManagerExt:
    """
    Base class for implementing extensions for a related manager defined with
    the given `related_name`.
    """

    def __new__(cls, data):
        if isinstance(data, Model):
            new = object.__new__(cls)
            new.instance = data
            return new
        else:
            return RelatedDescriptorExt(data, cls)

    def __init__(self, instance):
        super().__init__(instance)
