from codeschool import models
from codeschool.core.config import wagtail_root


def test_wagtail_root(db):
    root = wagtail_root()
    assert isinstance(root, models.Page)
    assert root.pk is not None
    assert root.path == '00010001'
