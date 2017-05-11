import pytest

from codeschool.lms.listings.score_map import \
    ScoreMap, ScoreTable, ScoreTableMapCommon

ScoreTableMapCommon._translate = lambda self, x: str(x)


@pytest.fixture
def score_map():
    m = ScoreMap('test1')
    m['foo'] = 5
    m['bar'] = 10
    m['foobar'] = 7
    return m


@pytest.fixture
def score_map2():
    m = ScoreMap('test2')
    m['foo'] = 7
    m['bar'] = 9
    m['ham'] = 7
    return m


@pytest.fixture
def score_table(score_map, score_map2):
    return ScoreTable([score_map, score_map2])


@pytest.fixture(params=[score_map,
                        lambda: score_table(score_map(), score_map2())])
def obj(request):
    return request.param()


def test_score_map_order(score_map):
    assert list(score_map) == ['foo', 'bar', 'foobar']


def test_can_sort_score_map(score_map):
    score_map.sort()
    assert list(score_map) == sorted(score_map)


def test_score_map_representation(score_map):
    assert str(score_map).splitlines() == [
        '<table class="lms--score-table">',
        '<tr><th>User</th><th>Grade</th></tr>',
        '<tr><td>foo</td><td>5<td></tr>',
        '<tr><td>bar</td><td>10<td></tr>',
        '<tr><td>foobar</td><td>7<td></tr>',
        '</table>',
    ]


def test_can_sort_score_table(score_table):
    score_table.sort()
    assert list(score_table) == sorted(score_table)


def test_score_table_order(score_table):
    assert list(score_table) == ['foo', 'bar', 'foobar', 'ham']


def test_score_sorted(obj):
    sorted = obj.sorted()
    assert sorted is not obj
    assert sorted == obj


def test_score_table_representation(score_table):
    assert str(score_table).splitlines() == [
        '<table class="lms--score-table">',
        '<tr><th>User</th><th>test1</th><th>test2</th></tr>',
        '<tr><td>foo</td><td>5</td><td>7</td></tr>',
        '<tr><td>bar</td><td>10</td><td>9</td></tr>',
        '<tr><td>foobar</td><td>7</td><td>0</td></tr>',
        '<tr><td>ham</td><td>0</td><td>7</td></tr>',
        '</table>',
    ]


def test_score_table_columns(score_map, score_map2, score_table):
    c1, c2 = score_table.iter_columns()
    score_map['ham'] = 0
    v = score_map2.pop('ham')
    score_map2['foobar'] = 0
    score_map2['ham'] = v

    assert dict(c1) == dict(score_map)
    assert c1.classes == score_map.classes
    assert str(c1) == str(score_map)
    assert c1 == score_map
    assert c2 == score_map2
