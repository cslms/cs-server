import collections
import os

from annoying.functions import get_config


class DebugInfo(collections.MutableMapping):
    """
    Stores debugging information about codeschool.

    Uses a mapping interface to expose info as key, value pairs.
    """

    def __init__(self, data=None, **kwargs):
        self._cache = {}
        self._keys = None
        self.update(data or {})
        self.update(kwargs)

    def __delitem__(self, key):
        raise KeyError('cannot delete keys')

    def __getitem__(self, key):
        try:
            return self._cache[key]
        except KeyError:
            pass

        if hasattr(self, key):
            data = getattr(self, key)()
            self._cache[key] = data
            return data
        else:
            raise KeyError(key)

    def __setitem__(self, key, value):
        if self._keys is None:
            self._update_keys()
        self._cache[key] = value
        self._keys.add(key)

    def __iter__(self):
        if self._keys is None:
            self._update_keys()
        return iter(self._keys)

    def __len__(self):
        if self._keys is None:
            self._update_keys()
        return len(self._keys)

    def _update_keys(self):
        blacklist = set(dir(collections.MutableMapping))
        self._keys = {
            name for name in dir(self)
            if name not in blacklist and not name.startswith('_')
        }

    #
    # Database
    #
    def dbfile(self):
        return get_config('DATABASES')['default']['NAME']

    def dbsize(self):
        size = os.path.getsize(self['dbfile'])
        return size

    def dbsize_mb(self):
        return self['dbsize'] / 1024 / 1024

    #
    # Auth
    #
    def num_users(self):
        from codeschool.models import User
        return User.objects.count()
