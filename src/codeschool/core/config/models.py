"""
This implements the db access used by DataDict and ConfigDict models.

These models should never be used directly. Instead use the dictionaries at
codeschool.core.config/data_store.
"""

import model_reference

from codeschool import models
from .config_dict import ConfigDict, DataDict


class KeyValuePair(models.Model):
    """
    Represents a (key, value) pair datum.
    """

    class Meta:
        abstract = True

    TYPE_STR, TYPE_INT, TYPE_FLOAT, TYPE_BOOL = range(4)
    name = models.CharField(max_length=30, unique=True)
    value = models.CharField(max_length=100)
    type = models.IntegerField(choices=[
        (TYPE_STR, 'str'),
        (TYPE_INT, 'int'),
        (TYPE_FLOAT, 'float'),
        (TYPE_BOOL, 'bool'),
    ])

    @property
    def data(self):
        raw_data = self.value
        if self.type == self.TYPE_STR:
            return raw_data
        elif self.type == self.TYPE_INT:
            return int(raw_data)
        elif self.type == self.TYPE_FLOAT:
            return float(raw_data)
        elif self.type == self.TYPE_BOOL:
            return bool(int(raw_data))
        else:
            raise ValueError(self.type)

    @classmethod
    def serialize(cls, value):
        """
        Return string representation of value.
        """

        try:
            return {
                int: str,
                float: str,
                str: lambda x: x,
                bool: lambda x: str(int(x))
            }[type(value)](value)
        except KeyError:
            type_name = value.__class__.__name__
            raise TypeError('invalid config value type: %r' % type_name)

    @classmethod
    def data_type(cls, value):
        """
        Return data type for value.
        """

        try:
            return {
                str: cls.TYPE_STR, int: cls.TYPE_INT,
                float: cls.TYPE_FLOAT, bool: cls.TYPE_BOOL,
            }[type(value)]

        except KeyError:
            type_name = value.__class__.__name__
            raise TypeError('invalid config value type: %r' % type_name)

    def __str__(self):
        return self.name


class ConfigOptionKeyValuePair(KeyValuePair):
    """
    Represents a (key, value) pair custom configuration.
    """


class DataEntryKeyValuePair(KeyValuePair):
    """
    Store arbitrary (key, value) data on the database.

    Separated from ConfigOptionKeyValuePair to hold non-configuration data.
    Each model lives in a different table.
    """


ConfigDict._key_value_pair_model = ConfigOptionKeyValuePair
DataDict._key_value_pair_model = DataEntryKeyValuePair


@model_reference.factory('root-page')
def wagtail_root_page():
    return models.Page.objects.get(path='00010001')
