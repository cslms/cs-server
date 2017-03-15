import collections


class ConfigDict(collections.MutableMapping):
    """
    A dictionary of options that is stored on the database.

    It accepts string keys and str, int and float values.
    """

    _model = None

    def __init__(self):
        self._cache = {}

    def __delitem__(self, key):
        try:
            option = self._model.objects.get(name=key)
        except self._model.DoesNotExist:
            raise KeyError(key)
        option.delete()
        self._cache.pop(key)

    def __getitem__(self, key):
        try:
            return self._cache[key]
        except KeyError:
            try:
                option = self._model.objects.get(name=key)
            except self._model.DoesNotExist:
                raise KeyError(key)
            self._cache[key] = result = option.data
            return result

    def __setitem__(self, key, value):
        data = self._model.serialize(value)
        data_type = self._model.data_type(value)
        try:
            option = self._model.objects.get(name=key)
        except self._model.DoesNotExist:
            option = self._model(name=key)
        option.type = data_type
        option.value = data
        option.save()
        self._cache[key] = value

    def __iter__(self):
        for option in self._model.objects.values_list('name', flat=True):
            yield option

    def __len__(self):
        return self._model.objects.count()


class DataDict(ConfigDict):
    """
    Dictionary wrapper for a different table.
    """
