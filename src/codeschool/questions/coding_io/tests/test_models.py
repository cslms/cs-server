import pytest
from django.core.exceptions import ValidationError

from codeschool.core import get_programming_language
from codeschool.questions.coding_io import factories
from codeschool.questions.coding_io.models.question import expand_tests

example = factories.question_from_example
source = factories.source_from_example


# Simple model creation
def test_simple_question_creation(db):
    question = example('simple')
    question.timeout = 0.5
    question.full_clean()
    question.full_clean_answer_keys()
    question.save()
    assert question.title == 'Hello Person'


def test_hello_question_creation(db):
    question = example('hello')
    question.full_clean_all()
    assert question.get_reference_source('python') == source('hello.py').strip()
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


# Validation
def test_do_not_validate_bad_pre_tests_source(db):
    question = example('simple')
    question.pre_tests_source = '$foo$'
    with pytest.raises(ValidationError) as ex:
        question.full_clean()
    assert 'pre_tests_source' in ex.value.args[0]


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


def test_validate_multiple_answer_keys(db):
    question = example('simple')
    question.answers.create(language=get_programming_language('c'),
                            source=source('hello.c'))
    question.full_clean_all()


def test_expand_iospec_source_with_commands(db):
    src = 'print(input("x: "))'
    question = example('hello-commands')
    question.full_clean_all()


# Expanding tests
def test_tests_expansion_fibonacci(db):
    question = example('fibonacci')
    tests = expand_tests(question, question.pre_tests)
    assert tests.is_simple
    assert tests.is_standard_test_case
