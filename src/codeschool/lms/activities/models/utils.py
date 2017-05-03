from django.apps import apps

from bricks.utils import snake_case


class AuxiliaryClassIntrospection:
    """
    Makes get_class(obj, name) works from class or from instance access.
    """

    def __init__(self, name, attr=None):
        self.name = name
        self.attr_name = attr or '%s_class' % name

    def __get__(self, instance, cls=None):
        result = getattr(cls._meta, self.attr_name, None)
        if result is None:
            result = get_class(cls, self.name)
            setattr(cls._meta, self.attr_name, result)
        return result


def get_class(cls, name):
    """
    Return class from a name. Used by progress_class, submission_class and
    response_class to compute automatic values.
    """

    class_name = getattr(cls._meta, '%s_class' % name)
    suffix = snake_case(cls.__name__).split('_')[-1].title()
    default_name = cls.__name__.replace(suffix, name.title())
    return apps.get_model(cls._meta.app_label, class_name or default_name)
