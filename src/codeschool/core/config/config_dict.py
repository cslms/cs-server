import collections


class ConfigDict(collections.MutableMapping):
    """
    A dictionary of options stored on the database.

    It accepts string keys and str, int and float values.
    """

    _key_value_pair_model = None

    def __init__(self):
        self._cache = {}

    def __delitem__(self, key):
        try:
            option = self._key_value_pair_model.objects.get(name=key)
        except self._key_value_pair_model.DoesNotExist:
            raise KeyError(key)
        option.delete()
        self._cache.pop(key)

    def __getitem__(self, key):
        try:
            return self._cache[key]
        except KeyError:
            try:
                option = self._key_value_pair_model.objects.get(name=key)
            except self._key_value_pair_model.DoesNotExist:
                raise KeyError(key)
            self._cache[key] = result = option.data
            return result

    def __setitem__(self, key, value):
        data = self._key_value_pair_model.serialize(value)
        data_type = self._key_value_pair_model.data_type(value)
        try:
            option = self._key_value_pair_model.objects.get(name=key)
        except self._key_value_pair_model.DoesNotExist:
            option = self._key_value_pair_model(name=key)
        option.type = data_type
        option.value = data
        option.save()
        self._cache[key] = value

    def __iter__(self):
        pairs = self._key_value_pair_model.objects
        for option in pairs.values_list('name', flat=True):
            yield option

    def __len__(self):
        return self._key_value_pair_model.objects.count()


class DataDict(ConfigDict):
    """
    Same as ConfigDict, but uses a separate table.
    """
