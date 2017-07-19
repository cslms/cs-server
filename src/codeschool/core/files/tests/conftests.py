import pytest

from codeschool.core.files import programming_language


@pytest.fixture
def python():
    return programming_language('python')


@pytest.fixture
def clang():
    return programming_language('c')
