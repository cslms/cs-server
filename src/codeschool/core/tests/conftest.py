import pytest

from codeschool.core import models


@pytest.fixture
def python():
    return models.programming_language('python')


@pytest.fixture
def clang():
    return models.programming_language('c')
