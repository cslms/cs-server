import pytest

from codeschool import models
from codeschool.core import get_wagtail_root
from codeschool.questions.coding_io.factories import \
    source_from_example as markio_example
from codeschool.cli.methods import push_resource_worker

pytestmark = pytest.mark.integration


@pytest.fixture
def auth(user, user_with_password, password):
    return (user_with_password, password)


@pytest.fixture
def question_root(db, auth):
    user = auth[0]
    root = get_wagtail_root()
    sub_page = models.Page(
        title='question root',
        slug='question-root',
        owner=user)
    root.add_child(instance=sub_page)
    return sub_page


def test_push_resource_worker(question_root, auth):
    data = markio_example('fibonacci.md')
    user, password = auth
    parent = question_root.slug
    page = push_resource_worker(data, 'coding_io/markio', parent, auth)

    assert page.owner == user
    assert page.url_path.endswith('question-root/fibonacci/')
