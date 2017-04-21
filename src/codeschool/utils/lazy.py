#
# Lazy evaluation
#
from lazyutils import *


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
