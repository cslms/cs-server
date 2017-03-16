from importlib import import_module

from django.core.exceptions import ImproperlyConfigured
from pyml.utils import snake_case



class HasProgressMixin:
    activity = property(lambda x: x.progress.activity)
    activity_id = property(lambda x: x.progress.activity_id)
    activity_title = property(lambda x: x.progress.activity_page.title)
    user = property(lambda x: x.progress.user)
    sender_username = property(lambda x: x.progress.user.username)


def subclass_registry(meta):
    """
    Return a new metaclass that inherits meta and register all sub-classes in
    the ._subclasses attribute.
    """

    class HasSubclassMeta(meta):
        """
        Register subclasses during class creation.
        """

        def __init__(cls, name, bases, ns):
            super().__init__(name, bases, ns)
            try:
                cls._subclasses.append(cls)
            except AttributeError:
                cls._subclasses = []

            if getattr(cls, '_subclass_root', None) is None:
                cls._subclass_root = cls.__name__
            if getattr(cls, '_subclass_related', None) is None:
                cls._subclass_related = []
            if not hasattr(cls, '_register_subclass'):
                cls._register_subclass = classmethod(_register_subclass)

    return HasSubclassMeta


def _register_subclass(cls):
    if cls.feedback_class is not None:
        return

    # Get models module
    models_path = cls.__module__.partition('.models')[0] + '.models'
    models = import_module(models_path)

    # Try importing feedback class
    cls_name = cls.__name__
    root_size = len(cls._subclass_root)
    if cls_name.endswith(cls._subclass_root):
        for attr in cls._subclass_related:
            related_name = cls_name[:-root_size] + attr
            related_attr = snake_case(related_name)
            try:
                related_cls = getattr(models, related_name)
                setattr(cls, related_attr, related_cls)
            except AttributeError:
                break
        else:
            return

    raise ImproperlyConfigured(
        'please define the feedback_class attribute in %s' % cls_name
    )
