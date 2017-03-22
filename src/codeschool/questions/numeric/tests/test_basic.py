import pytest

from codeschool.questions.numeric.factories import make_numeric_question, \
    make_numeric_question_fuzzy


@pytest.fixture
def question_42(db):
    return make_numeric_question()


def test_make_numeric_question(db):
    make_numeric_question()


def test_make_numeric_question_fuzzy(db):
    question = make_numeric_question_fuzzy()
    assert question.title == 'Pie'


def test_correct_submission(rf, question_42, user):
    request = rf.get(question_42.url)
    request.user = user
    submission = question_42.submit(request, value=42)
    feedback = submission.autograde()
    assert feedback.is_correct


def test_wrong_submission(rf, question_42, user):
    request = rf.get(question_42.url)
    request.user = user
    submission = question_42.submit(request, value=43)
    feedback = submission.autograde()
    assert not feedback.is_correct
