import pytest

from codeschool.questions.text.factories import make_text_question, \
    make_regex_text_question

pytestmark = pytest.mark.test_db


@pytest.fixture
def question_first(db):
    return make_text_question()


@pytest.fixture
def question_regex(db):
    return make_regex_text_question()
