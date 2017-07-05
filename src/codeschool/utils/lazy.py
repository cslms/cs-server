#
# Lazy evaluation
#
from lazyutils import lazy, lazy_classattribute, lazy_shared, alias  # noqa
from lazyutils import delegate_ro, delegate_to, readonly  # noqa


class delegate_to_or_none(delegate_to):  # noqa: N801
    """
    Like delegate_to(), but return None if delegate is None.

    Examples:

        >>> class Breakfast:
        ...     data = {'ham': 'spam', 'bacon': 'eggs'}
        ...     key = delegate_to_or_none("data")
        >>> x = Breakfast()
        >>> x.key('ham')
        'spam'
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
