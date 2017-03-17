import pytest

from codeschool.core import get_programming_language
from codeschool.core.models import ProgrammingLanguage


def test_get_language_support_most_common_languages(db):
    assert get_programming_language('python').name == 'Python 3.5'
    assert get_programming_language('python2').name == 'Python 2.7'


def test_c_language_aliases(db):
    lang = get_programming_language
    assert lang('c') == lang('gcc')
    assert lang('cpp') == lang('g++')


def test_new_unsupported_language(db):
    # Explicit mode
    with pytest.raises(ProgrammingLanguage.DoesNotExist):
        get_programming_language('foolang')

    # Silent mode
    lang = get_programming_language('foolang', raises=False)
    assert lang.ref == 'foolang'
    assert lang.name == 'Foolang'
    assert lang.is_supported is False
    assert lang.is_language is True
    assert lang.is_binary is False
