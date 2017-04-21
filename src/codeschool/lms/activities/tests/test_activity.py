import pytest

from codeschool import get_wagtail_root
from codeschool.lms.activities.models import Activity


@pytest.fixture
def activity(db):
    page = Activity(title='Test')
    get_wagtail_root().add_child(instance=page)
    return page
