import pytest
from django.core.exceptions import ValidationError

from codeschool.questions.numeric.factories import make_numeric_question_42, \
    make_numeric_question_pi

pytestmark = pytest.mark.integration


@pytest.fixture
def question_42(db):
    return make_numeric_question_42()


@pytest.fixture
def question_pi(db):
    return make_numeric_question_pi()


def test_create_titleless_question(db, question_42):
    question_42.full_clean()

    with pytest.raises(ValidationError):
        question_42.title = ''
        question_42.full_clean()


def test_make_numeric_question(db):
    question = make_numeric_question_42()
    assert question.correct_answer == 42


def test_make_numeric_question_fuzzy(db):
    question = make_numeric_question_pi()
    assert question.title == 'Pie'


def test_correct_submission(rf, question_42, user):
    """
    User can make a correct submission.
    """
    request = rf.get(question_42.url)
    request.user = user
    submission = question_42.submit(request, value=42)
    feedback = submission.auto_feedback()
    assert feedback.is_correct


def test_wrong_submission(rf, question_42, user):
    request = rf.get(question_42.url)
    request.user = user
    submission = question_42.submit(request, value=43)
    feedback = submission.auto_feedback()
    assert not feedback.is_correct


def test_value_within_tolerance(rf, question_pi, user):
    request = rf.get(question_pi.url)
    request.user = user
    submission = question_pi.submit(request, value=3.14)
    feedback = submission.auto_feedback()
    assert feedback.is_correct
    assert feedback.given_grade_pc == 100


def test_value_outside_tolerance(rf, question_pi, user):
    request = rf.get(question_pi.url)
    request.user = user
    submission = question_pi.submit(request, value=3.25)
    feedback = submission.auto_feedback()
    assert not feedback.is_correct
    assert feedback.given_grade_pc == 0
