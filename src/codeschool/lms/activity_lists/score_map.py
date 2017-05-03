"""
ScoreMap and ScoreTable are HTML-representable data structures that maps
students to their specific grades.
"""
import collections
import copy

from django.utils.html import escape
from django.utils.translation import ugettext_lazy as _


class ScoreTableMapCommon(collections.Mapping):
    """
    Common implementations to ScoreMap and ScoreTable.
    """

    default_class = 'lms--score-table'

    def __init__(self, data=None, classes=None):
        self._data = self._data = collections.OrderedDict(data or {})
        if classes is None:
            classes = (self.default_class,)
        self.classes = list(classes)

    def __iter__(self):
        return iter(self._data)

    def __len__(self):
        return len(self._data)

    def __str__(self):
        return self.__html__()

    def __getitem__(self, key):
        return self._data[key]

    def __delitem__(self, key):
        self.pop(key)

    def __html__(self):
        raise NotImplementedError

    def __eq__(self, other):
        if isinstance(other, type(self)):
            return self.__html__() == other.__html__()
        return NotImplemented

    def _table_tag(self):
        if self.classes:
            return '<table class="%s">' % (' '.join(self.classes))
        else:
            return '<table>'

    def _key_render(self, key):
        """
        Computes key name from key value. Useful for subclassing.
        """

        if isinstance(key, str):
            return escape(key)
        return escape(key.get_full_name() or key.username)

    def _value_render(self, value):
        """
        Computes HTML safe representation of value. Useful for subclassing.
        """

        if isinstance(value, str):
            return escape(value)
        return '%d' % value

    def pop(self, key):
        return self._data.pop(key)

    def sort(self, key='username'):
        """
        Sort *INPLACE* using the given key function.

        If key='username' (default), sort by username. If key='grade', sort by
        grade value. Otherwise key must be a function that receives a pair
        of (user, grade_value).
        """

        if key == 'username':
            def key(item):
                return self._key_render(item[0])

        data = list(self.items())
        data.sort(key=key)
        self._data.clear()
        self._data.update(data)

    def sorted(self, key='username'):
        """
        Return a sorted version of score map.
        """

        data = self._data.copy()
        new = copy.copy(self)
        new._data = data
        return new

    def _translate(self, st):
        """
        Translate string
        """

        return _(st)

    def to_csv(self, sep=','):
        """
        Convert data to CSV.
        """

        raise NotImplementedError


class ScoreMap(ScoreTableMapCommon):
    """
    A mapping between users and grades.
    """

    def __init__(self, name, data=None, classes=("lms--score-table",)):
        self.name = name
        super().__init__(data, classes)

    def __setitem__(self, key, value):
        self._data[key] = value

    def __eq__(self, other):
        if isinstance(other, type(self)):
            return other.name == self.name and super().__eq__(other)
        return super().__eq__(other)

    def __html__(self):
        _ = self._translate
        key_trans = self._key_render
        value_trans = self._value_render

        def html_row(key, value):
            user = key_trans(key)
            grade = value_trans(value)
            return '<tr><td>%s</td><td>%s<td></tr>' % (user, grade)

        col_names = _('User'), _('Grade')
        tags = [
            self._table_tag(),
            '<tr><th>%s</th><th>%s</th></tr>' % col_names,
        ]

        for k, v in self._data.items():
            tags.append(html_row(k, v))
        tags.append('</table>')
        return '\n'.join(tags)

    def sort(self, key='username'):
        if key == 'grade':
            def key(item):
                return item[1]
        super().sort(key=key)

    def to_csv(self, sep=','):
        key_trans = self._key_render
        value_trans = self._value_render
        rows = []
        for k, v in self._data.items():
            row = '%s%s%s' % (key_trans(k), sep, value_trans(v))
            rows.append(row)
        return '\n'.join(rows)


class ScoreTable(ScoreTableMapCommon):
    """
    A table mapping users to a list of grades.
    """

    def __init__(self, columns=None, default=0, name=None):
        super().__init__()
        self._columns = []
        self.default = default
        self.name = name
        if columns:
            for col in columns:
                self.add_column(col)

    def __html__(self):
        _ = self._translate
        key_trans = self._key_render
        value_trans = self._value_render

        def html_row(key, value):
            user = key_trans(key)
            data = ['<tr><td>%s</td>' % user]
            for grade in value:
                grade = value_trans(grade)
                data.append('<td>%s</td>' % grade)
            data.append('</tr>')
            return ''.join(data)

        tags = [self._table_tag()]
        aux = ['<tr><th>%s</th>' % _('User')]
        for col in self._columns:
            aux.append('<th>%s</th>' % col)
        aux.append('</tr>')
        tags.append(''.join(aux))

        for k, v in self._data.items():
            tags.append(html_row(k, v))
        tags.append('</table>')
        return '\n'.join(tags)

    def iter_columns(self):
        """
        Iterate over ScoreMap column instances.
        """

        items = list(self.items())
        for idx, col in enumerate(self._columns):
            data = collections.OrderedDict((k, v[idx]) for (k, v) in items)
            yield ScoreMap(col, data=data, classes=self.classes)

    def add_column(self, col):
        """
        Adds a new ScoreMap column to the right.
        """

        data = collections.OrderedDict(col)
        default = self.default
        n_cols = len(self._columns)
        self._columns.append(col.name)
        for k, v in data.items():
            try:
                self[k].append(v)
            except KeyError:
                self._data[k] = lst = [default] * n_cols
                lst.append(v)
        for k, v in self._data.items():
            if k not in data:
                v.append(default)

    def add_total(self, name='total', method='mean'):
        """
        Add a new column with the totals computed using the given method.

        Args:
            name (str):
                Column's name
            method (callable/str):
                Can be a callable that receives a list of numbers and return
                their reduction or one of the strings: 'mean', 'sum', 'max',
                or 'min'.

        Return:
            A ScoreMap element for the newly added column.
        """

        # Chose the appropriate reduction method.
        if isinstance(method, str):
            try:
                method = {
                    'mean': lambda x: sum(x) / len(x),
                    'mean-skip': lambda x: (sum(x) - min(x)) / (len(x) - 1),
                    'sum': sum,
                    'max': max,
                    'min': min,
                }[method]
            except KeyError:
                raise ValueError('invalid method: %r' % method)

        col = ScoreMap(name)
        for key, value in self.items():
            col[key] = method(value)
        self.add_column(col)
        return col

    def sort(self, key='username'):
        n_cols = len(self._columns)
        if key == 'mean':
            def key(item):
                return sum(item[1]) / n_cols
        super().sort(key=key)

    def to_csv(self, sep=','):
        key_trans = self._key_render
        value_trans = self._value_render
        rows = []
        for k, v in self._data.items():
            row_body = sep.join(map(value_trans, v))
            row = '%s%s%s' % (key_trans(k), sep, row_body)
            rows.append(row)
        return '\n'.join(rows)


def score_board(activity, users=None, info=None):
    """
    Return a mapping between users and their respective grades.

    Args:
        activity:
            An activity instance.
        users:
            Filter users to the given set. The default behavior is to
            include all users that made any single submission.
        info ('points', 'grade', 'stars', 'score'):
            The information used to construct the score board.
    """

    info = info or 'points'
    if info not in ['points', 'grade', 'stars', 'score']:
        raise ValueError('invalid info: %r' % info)

    if users is None:
        users = activity.users()

    board = ScoreMap(activity.title)
    for user in users:
        response = activity.responses.response_for_user(user)
        board[user] = getattr(response, info)
    return board
