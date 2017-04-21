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
