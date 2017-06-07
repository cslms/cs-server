import pytest
from django.core.exceptions import ValidationError
from markio import parse_markio
from codeschool.questions.coding_io.ejudge import expand_from_code
from iospec import parse, Out, In, StandardTestCase

from codeschool.core import get_programming_language
from codeschool.lms.activities.models import Feedback
from codeschool.questions.coding_io import factories
from codeschool.questions.coding_io.models.question import expand_tests

pytestmark = pytest.mark.integration
example = factories.question_from_example
source = factories.source_from_example


@pytest.mark.skip
def test_dump_markio_exports_successfully(db):
    question = example('simple')
    md_source = question.dump_markio()
    md = parse_markio(source('simple.md'))
    assert md_source == md.source()


def test_submission_correct_response_hello(db, user, request_with_user):
    question = example('simple')
    src = source('hello.py')
    submission = question.submit(request_with_user,
                                 source=src,
                                 language='python')
    feedback = submission.auto_feedback()
    assert feedback.given_grade_pc == 100
    assert feedback.final_grade_pc == 100
    assert feedback.is_correct is True


def test_submission_correct_response_fibonacci(db, user, request_with_user):
    question = example('fibonacci')
    src = source('fibonacci.py')
    submission = question.submit(request_with_user,
                                 source=src,
                                 language='python')
    feedback = submission.auto_feedback()
    assert feedback.is_correct is True


def test_submission_with_presentation_error_hello(db, user, request_with_user):
    question = example('simple')
    submission = question.submit(request_with_user,
                                 source=source('hello-presentation.py'),
                                 language='python')
    feedback = submission.auto_feedback()
    assert feedback.is_correct is False
    assert feedback.feedback_status == 'presentation-error'
    assert feedback.is_presentation_error
    assert feedback.given_grade_pc < 100


def test_submission_with_wrong_answer_hello(db, user, request_with_user):
    question = example('simple')
    submission = question.submit(request_with_user,
                                 source=source('hello-wrong.py'),
                                 language='python')
    feedback = submission.auto_feedback()
    assert feedback.is_correct is False
    assert feedback.feedback_status == 'wrong-answer'
    assert feedback.is_wrong_answer
    assert feedback.final_grade_pc == 0


def test_submission_with_runtime_error_hello(db, user, request_with_user):
    question = example('simple')
    submission = question.submit(request_with_user,
                                 source=source('hello-runtime.py'),
                                 language='python')
    feedback = submission.auto_feedback()
    assert feedback.is_correct is False
    assert feedback.feedback_status == 'runtime-error'
    assert feedback.is_runtime_error
    assert feedback.final_grade_pc == 0


def test_submission_with_invalid_syntax_hello(db, user, request_with_user):
    question = example('simple')
    submission = question.submit(request_with_user,
                                 source=source('hello-build.py'),
                                 language='python')
    feedback = submission.auto_feedback()
    assert feedback.is_correct is False
    assert feedback.feedback_status == 'build-error'
    assert feedback.is_build_error
    assert feedback.final_grade_pc == 0


def test_submission_feedback_keeps_the_correct_code_hello(db, user,
                                                          request_with_user):
    question = example('simple')
    submission = question.submit(request_with_user,
                                 source=source('hello-build.py'),
                                 language='python')
    feedback = submission.auto_feedback()
    db_fb = Feedback.objects.get(id=submission.id)
    assert feedback.feedback_status == db_fb.feedback.status


@pytest.mark.skip('ejduge not catching timeout errors?')
def test_stop_execution_of_submission_after_timeout_hello(db, user,
                                                          request_with_user):
    question = example('simple')
    question.timeout = 0.35

    submission = question.submit(request_with_user,
                                 source=source('hello-timeout.py'),
                                 language='python')
    feedback = submission.auto_feedback()
    assert feedback.is_correct is False
    assert feedback.feedback_status == 'timeout-error'
    assert feedback.is_timeout_error
    assert feedback.final_grade_pc == 0


# Test expansions
def test_tests_expansion_fibonacci(db):
    question = example('fibonacci')
    tests = expand_tests(question, question.pre_tests)
    assert tests.is_simple
    assert tests.is_standard_test_case


def test_expand_iospec_source_with_commands(db):
    src = 'print(input("x: "))'
    question = example('hello-commands')
    question.full_clean_all()


def test_hello_question_creation(db):
    question = example('hello')
    question.full_clean_all()
    assert question.get_reference_source(
        'python') == source('hello.py').strip()
    assert question.title == 'Hello Person'
    assert question.pre_tests is not None
    assert question.pre_tests.is_expanded is True
    assert question.post_tests is not None
    assert question.post_tests.is_expanded is False
    assert question.answers.count() == 1


def test_fibonacci_question_creation(db):
    question = example('fibonacci')
    question.full_clean_all()
    assert question.pre_tests is not None
    assert question.pre_tests.is_expanded is False
    assert question.post_tests is not None
    assert question.post_tests.is_expanded is False
    assert question.answers.count() == 1


# Simple model creation
def test_simple_question_creation(db):
    question = example('simple')
    question.timeout = 0.5
    question.full_clean()
    question.full_clean_answer_keys()
    question.save()
    assert question.title == 'Hello Person'


# Validation
def test_do_not_validate_bad_pre_tests_source(db):
    question = example('simple')
    question.pre_tests_source = '$foo$'
    with pytest.raises(ValidationError) as ex:
        question.full_clean()
    assert 'pre_tests_source' in ex.value.args[0]

def test_validate_multiple_answer_keys(db):
    question = example('simple')
    question.answers.create(language=get_programming_language('c'),
                            source=source('hello.c'))
    question.full_clean_all()

def test_expand_from_code_keep_simple_cases():
    src = "print(input('x:'))"
    iospec = (
        'x: <foo>\n'
        'foo\n'
        '\n'
        '@input $name\n'
        '\n'
        'x: <bar>\n'
        'bar'
    )
    iospec = parse(iospec)
    expanded = expand_from_code(src, iospec, lang='python')
    expected = StandardTestCase([Out('x: '), In('foo'), Out('foo')])
    assert expanded[0] == expected

def test_do_not_validate_negative_timeout(db):
    question = example('simple')
    question.timeout = - 1
    with pytest.raises(ValidationError) as ex:
        question.full_clean()
    assert 'timeout' in ex.value.args[0]

    question.timeout = 0
    with pytest.raises(ValidationError) as ex:
        question.full_clean()
    assert 'timeout' in ex.value.args[0]