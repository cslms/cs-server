from collections import Sequence

from lazyutils import lazy


class Statistics(Sequence):
    """
    An object that computes a series of statistical data over some data set.
    """

    def __init__(self, name, data, default=0):
        self.name = name
        self.data = list(data)
        self.default = default

    @lazy
    def _sorted(self):
        """
        Cache sorted values with no given key function.
        """

        return sorted(self.data)

    def __len__(self):
        return len(self.data)

    def __iter__(self):
        return iter(self.data)

    def __getitem__(self, idx):
        return self.data[idx]

    def max(self, key=lambda x: x, default=None):
        """
        Return the greatest value in data.
        """

        default = 0 if default is None else self.default
        return max(self.data, key=key, default=default)

    def min(self, key=lambda x: x, default=None):
        """
        Return the smallest value in data.
        """

        default = 0 if default is None else self.default
        return min(self.data, key=key, default=default)

    def sum(self, default=None):
        """
        Return the sum of all data values.
        """

        default = 0 if default is None else self.default
        return sum(self.data, default)

    def mean(self, default=None):
        """
        Return the mean value from data
        """

        return self.sum(default) / len(self.data)

    def sorted(self, key=lambda x: x):
        """
        Return a list with all data values sorted by the given key function.
        """

        return self._sorted if key is None else sorted(self.data, key=key)

    def median(self, key=lambda x: x):
        """
        Median of the data set using key function to sort values
        """

        sorted_data = self.sorted(key)
        n = len(sorted_data)
        if n % 2:
            return sorted_data[n // 2]
        elif n == 0:
            raise ValueError('empty data set has no median')
        else:
            return (sorted_data[n // 2] + sorted_data[n // 2 - 1]) / 2
