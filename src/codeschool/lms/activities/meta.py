from wagtail.wagtailcore.models import PageBase


class ActivityMeta(PageBase):
    """
    Metaclass for Activity
    """

    EXTRA_META_VARS = {
        'instant_feedback': True,
        'automatic_grading': True,
        'progress_class': None,
        'submission_class': None,
        'feedback_class': None,
    }

    def __new__(metaclass, name, bases, namespace):
        meta = namespace.get('Meta', None)
        extra_fields, meta = metaclass._extract_extra_meta_fields(meta)
        if 'Meta' in namespace:
            namespace['Meta'] = meta
        cls = super().__new__(metaclass, name, bases, namespace)
        cls._update_extra_meta_fields(extra_fields)
        return cls

    @classmethod
    def _extract_extra_meta_fields(metaclass, meta):
        if meta is None:
            return None, None

        vars = {attr: getattr(meta, attr, None) for attr in dir(meta)}
        fields = {k: v for k, v in vars.items() if
                  k in metaclass.EXTRA_META_VARS}
        fields = dict(metaclass.EXTRA_META_VARS, **fields)
        vars = {k: v for k, v in vars.items() if
                k not in metaclass.EXTRA_META_VARS}
        meta = type('Meta', (), vars)
        return fields, meta

    def _update_extra_meta_fields(cls, fields):
        meta = cls._meta
        for subclass in cls.__mro__:
            if hasattr(subclass, '_meta'):
                for attr, value in cls.EXTRA_META_VARS.items():
                    setattr(meta, attr, value)
                break

        for attr, value in fields.items():
            setattr(meta, attr, value)
