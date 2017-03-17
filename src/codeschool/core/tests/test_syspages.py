import pytest

from codeschool.models import Page
from codeschool.core import models, get_wagtail_root


def test_wagtail_root(db):
    root = get_wagtail_root()
    assert isinstance(root, Page)
    assert root.pk is not None
    assert root.path == '00010001'
