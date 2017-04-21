from django.apps import apps


def get_class(obj, name):
    """
    Return class from a name. Used by progress_class, submission_class and
    response_class to compute automatic values.
    """

    cls = getattr(obj._meta, '%s_class' % name)
    if isinstance(cls, type):
        return cls
    else:
        return apps.get_model(
            obj._meta.app_label,
            cls or obj.__class__.__name__.replace('Question', name.title())
        )
