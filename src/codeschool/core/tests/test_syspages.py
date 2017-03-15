import pytest

from codeschool.models import Page
from codeschool.core import models


def _test_page(page):
    assert isinstance(page, Page)
    assert page.pk is not None


@pytest.mark.django_db
def test_rogue_root(db):
    page = models.RogueRoot.instance()
    _test_page(page)


@pytest.mark.django_db
def test_hidden_root(db):
    page = models.HiddenRoot.instance()
    _test_page(page)
    assert page.live is False
