import pytest

from codeschool.questions.numeric.factories import make_numeric_question, \
    make_numeric_question_fuzzy


@pytest.fixture
def question_42(db):
    return make_numeric_question()

@pytest.fixture
def question_pi(db):
    return make_numeric_question_fuzzy()

def test_create_titleless_question(db):
    with pytest.raises(Exception):
        make_titleless_question()

def test_create_big_title_question(db):
    with pytest.raises(Exception):
        make_big_title_question()

def test_make_numeric_question(db):
    question = make_numeric_question()
    assert question.correct_answer == 42

def test_make_numeric_question_fuzzy(db):
    question = make_numeric_question_fuzzy()
    assert question.title == 'Pie'


def test_correct_submission(rf, question_42, user):
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

def test_less_than_tolerance(rf, question_pi, user):
    request = rf.get(question_pi.url)
    request.user = user
    submission = question_pi.submit(request, value=3.13)
    feedback = submission.autograde()
    assert not feedback.is_correct

def test_equal_tolerance(rf, question_pi, user):
    request = rf.get(question_pi.url)
    request.user = user
    submission = question_pi.submit(request, value=3.14)
    feedback = submission.autograde()
    assert feedback.is_correct
    assert feedback.given_grade_pc == 100

def test_higher_than_tolerance(rf, question_pi, user):
    request = rf.get(question_pi.url)
    request.user = user
    submission = question_pi.submit(request, value=3.25)
    feedback = submission.autograde()
    assert not feedback.is_correct
    assert feedback.given_grade_pc == 0
