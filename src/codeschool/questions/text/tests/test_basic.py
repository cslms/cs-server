import pytest

from codeschool.questions.text.factories import make_text_questions, \
    make_text_questions_fuzzy


@pytest.fixture
def question_first(db):
    return make_text_questions()


def test_make_text_question(db, user):
    question = make_text_questions()
    assert question.title == 'The Answer'

def test_correct_submission_text_question(rf, question_first, user):
    request = rf.get(question_first.url)
    request.user = user
    submission = question_first.submit(request, value='Quarenta e três')
    feedback = submission.auto_feedback()
    assert feedback.is_correct


def test_incorrect_submission_text_question(rf, question_first, user):
    request = rf.get(question_first.url)
    request.user = user
    submission = question_first.submit(request, value='Quarenta e um')
    feedback = submission.auto_feedback()
    assert not feedback.is_correct

def test_correct_uppercase_submition_text_question(rf, question_first, user):
    request = rf.get(question_first.url)
    request.user = user
    submission = question_first.submit(request, value='QUARENTA E TRÊS')
    feedback = submission.auto_feedback()
    assert feedback.is_correct

def test_incorrect_uppercase_submition_text_question(rf, question_first, user):
    request = rf.get(question_first.url)
    request.user = user
    submission = question_first.submit(request, value='QUARENTA E UM')
    feedback = submission.auto_feedback()
    assert not feedback.is_correct

def test_correct_lowercase_submition_text_question(rf, question_first, user):
    request = rf.get(question_first.url)
    request.user = user
    submission = question_first.submit(request, value='quarenta e três')
    feedback = submission.auto_feedback()
    assert feedback.is_correct

def test_incorrect_lowercase_submition_text_question(rf, question_first, user):
    request = rf.get(question_first.url)
    request.user = user
    submission = question_first.submit(request, value='quarenta e um')
    feedback = submission.auto_feedback()
    assert not feedback.is_correct
