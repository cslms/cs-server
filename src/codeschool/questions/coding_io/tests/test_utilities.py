from codeschool.questions.coding_io.ejudge import expand_from_code
from iospec import parse, Out, In, StandardTestCase


def test_expand_from_code_keep_simple_cases():
    src = "print(input('x:'))"
    iospec = (
        'x: <foo>\n'
        'foo\n'
        '\n'
        '@input $name\n'
        '\n'
        'x: <bar>\n'
        'bar'
    )
    iospec = parse(iospec)
    expanded = expand_from_code(src, iospec, lang='python')
    expected = StandardTestCase([Out('x: '), In('foo'), Out('foo')])
    assert expanded[0] == expected
