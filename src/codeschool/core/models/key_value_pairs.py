"""
This implements the db access used by DataDict and ConfigDict models.

These models should never be used directly. Instead use the dictionaries at
codeschool.core.config/data_store.
"""

from codeschool import models
from codeschool.core import DataDict, ConfigDict


class KeyValuePair(models.Model):
    """
    Represents a (key, value) pair datum.
    """

    class Meta:
        abstract = True

    name = models.CharField(max_length=30, unique=True)
    value = models.CharField(max_length=100)
    type = models.IntegerField(choices=[
        (0, 'str'),
        (1, 'int'),
        (2, 'float'),
        (3, 'bool'),
    ])

    @property
    def data(self):
        raw_data = self.value
        if self.type == 0:
            return raw_data
        elif self.type == 1:
            return int(raw_data)
        elif self.type == 2:
            return float(raw_data)
        elif self.type == 3:
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
            return {str: 0, int: 1, float: 2, bool: 3}[type(value)]
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
    """

ConfigDict._key_value_pair_model = ConfigOptionKeyValuePair
DataDict._key_value_pair_model = DataEntryKeyValuePair
