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
    submission = question_first.submit(request, value='joão')
    feedback = submission.autograde()
    assert feedback.is_correct


def test_incorrect_submission_text_question(rf, question_first, user):
    request = rf.get(question_first.url)
    request.user = user
    submission = question_first.submit(request, value='alo')
    feedback = submission.autograde()
    assert not feedback.is_correct


