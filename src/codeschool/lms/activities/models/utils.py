from django.apps import apps


class AuxiliaryClassIntrospection:
    """
    Makes get_class(obj, name) works from class or from instance access.
    """

    def __init__(self, name, attr=None):
        self.name = name
        self.attr_name = attr or '%s_class' % name
        self.value = None

    def __get__(self, instance, cls=None):
        if self.value is None:
            self.value = get_class(cls, self.name)
        return self.value


def get_class(obj, name):
    """
    Return class from a name. Used by progress_class, submission_class and
    response_class to compute automatic values.
    """

    class_name = getattr(obj._meta, '%s_class' % name)
    if isinstance(class_name, type):
        return class_name
    else:
        cls = obj if isinstance(obj, type) else obj.__class__
        default_name = cls.__name__.replace('Question', name.title())
        return apps.get_model(obj._meta.app_label, class_name or default_name)
