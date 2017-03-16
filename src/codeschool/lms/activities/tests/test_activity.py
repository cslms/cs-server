import pytest

from codeschool import rogue_root
from codeschool.lms.activities.models import Activity


@pytest.fixture
def activity(db):
    page = Activity(title='Test')
    rogue_root().add_child(instance=page)
    return page


