import pytest

from codeschool.lms.activities.models import Feedback
from codeschool.questions.coding_io.tests.test_models import example, source


def test_submission_correct_response_hello(db, user, request_with_user):
    question = example('simple')
    src = source('hello.py')
    submission = question.submit(request_with_user,
                                 source=src,
                                 language='python')
    feedback = submission.autograde()
    assert feedback.given_grade_pc == 100
    assert feedback.final_grade_pc == 100
    assert feedback.is_correct is True


def test_submission_correct_response_fibonacci(db, user, request_with_user):
    question = example('fibonacci')
    src = source('fibonacci.py')
    submission = question.submit(request_with_user,
                                 source=src,
                                 language='python')
    feedback = submission.autograde()
    assert feedback.is_correct is True


def test_submission_with_presentation_error_hello(db, user, request_with_user):
    question = example('simple')
    submission = question.submit(request_with_user,
                                 source=source('hello-presentation.py'),
                                 language='python')
    feedback = submission.autograde()
    assert feedback.is_correct is False
    assert feedback.feedback_status == 'presentation-error'
    assert feedback.is_presentation_error
    assert feedback.given_grade_pc < 100


def test_submission_with_wrong_answer_hello(db, user, request_with_user):
    question = example('simple')
    submission = question.submit(request_with_user,
                                 source=source('hello-wrong.py'),
                                 language='python')
    feedback = submission.autograde()
    assert feedback.is_correct is False
    assert feedback.feedback_status == 'wrong-answer'
    assert feedback.is_wrong_answer
    assert feedback.final_grade_pc == 0


def test_submission_with_runtime_error_hello(db, user, request_with_user):
    question = example('simple')
    submission = question.submit(request_with_user,
                                 source=source('hello-runtime.py'),
                                 language='python')
    feedback = submission.autograde()
    assert feedback.is_correct is False
    assert feedback.feedback_status == 'runtime-error'
    assert feedback.is_runtime_error
    assert feedback.final_grade_pc == 0


def test_submission_with_invalid_syntax_hello(db, user, request_with_user):
    question = example('simple')
    submission = question.submit(request_with_user,
                                 source=source('hello-build.py'),
                                 language='python')
    feedback = submission.autograde()
    assert feedback.is_correct is False
    assert feedback.feedback_status == 'build-error'
    assert feedback.is_build_error
    assert feedback.final_grade_pc == 0


def test_submission_feedback_keeps_the_correct_code_hello(db, user, request_with_user):
    question = example('simple')
    submission = question.submit(request_with_user,
                                 source=source('hello-build.py'),
                                 language='python')
    feedback = submission.autograde()
    db_fb = Feedback.objects.get(id=submission.id)
    assert feedback.feedback_status == db_fb.feedback.status


@pytest.mark.skip('ejduge not catching timeout errors?')
def test_stop_execution_of_submission_after_timeout_hello(db, user, request_with_user):
    question = example('simple')
    question.timeout = 0.35

    submission = question.submit(request_with_user,
                                 source=source('hello-timeout.py'),
                                 language='python')
    feedback = submission.autograde()
    assert feedback.is_correct is False
    assert feedback.feedback_status == 'timeout-error'
    assert feedback.is_timeout_error
    assert feedback.final_grade_pc == 0