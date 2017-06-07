from wagtail.wagtailcore.models import PageBase

EXTRA_META_VARS = {
    'instant_feedback': True,
    'autograde': True,
    'progress_class': None,
    'submission_class': None,
    'feedback_class': None,
}


class ActivityMeta(PageBase):
    """
    Metaclass for Activity
    """

    def __new__(metaclass, name, bases, namespace):
        meta = namespace.get('Meta')
        extra_fields, meta = extract_extra_meta_fields(meta)
        if 'Meta' in namespace:
            namespace['Meta'] = meta
        cls = super().__new__(metaclass, name, bases, namespace)
        update_extra_meta_fields(cls, extra_fields)
        return cls


def extract_extra_meta_fields(meta):
    if meta is None:
        return None, None

    vars = {attr: getattr(meta, attr, None) for attr in dir(meta)}
    fields = {k: v for k, v in vars.items() if
              k in EXTRA_META_VARS}
    fields = dict(EXTRA_META_VARS, **fields)
    vars = {k: v for k, v in vars.items() if
            k not in EXTRA_META_VARS}
    meta = type('Meta', (), vars)
    return fields, meta


def update_extra_meta_fields(cls, fields):
    meta = cls._meta
    fields = fields or {}
    for subclass in cls.__mro__:
        if hasattr(subclass, '_meta'):
            for attr, value in EXTRA_META_VARS.items():
                setattr(meta, attr, value)
            break

    for attr, value in fields.items():
        setattr(meta, attr, value)
