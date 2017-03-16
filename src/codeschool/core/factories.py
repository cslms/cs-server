import os

import model_reference
from mommys_boy import DjangoModelFactory, LazyAttributeSequence

import codeschool.questions
from codeschool import settings
from codeschool.core import models

#
# File formats
#
from codeschool.questions.coding_io.models import CodingIoQuestion


class ProgrammingLanguageFactory(DjangoModelFactory):
    class Meta:
        model = models.ProgrammingLanguage

    ref = LazyAttributeSequence(lambda x: 'lang%s' % x)
    name = LazyAttributeSequence(lambda x: 'Lang-%s' % x)


def make_question_from_markio_example(path, parent=None):
    base = os.path.dirname(codeschool.questions.coding_io.__file__)
    path = os.path.join(base, 'examples', path)
    question = CodingIoQuestion.import_markio_from_path(path, parent)
    return question


def make_hello_world_question(parent=None):
    question = CodingIoQuestion(
        title='Hello World',
        body=[
            ('markdown',
             'The most basic operation you can do in most programming '
             'languages is to display some message on the screen. Create a '
             'program that shows `hello world!` when executed.'),
        ],
        pre_tests_source='hello world!',
    )
    parent = parent or model_reference.load('main-question-list')
    parent.add_child(instance=question)
    return question


def make_example_questions(parent):
    basic = parent.get_children().get(slug='basic')
    loops = parent.get_children().get(slug='loops')
    questions = []

    # Coding Io questions
    if 'codeschool.questions.coding_io' in settings.INSTALLED_APPS:
        questions.extend([
            make_hello_world_question(basic),
            make_question_from_markio_example('simple.md', basic),
            make_question_from_markio_example('fibonacci.md', loops)
        ])

    # Numeric questions
    if 'codeschool.questions.numeric' in settings.INSTALLED_APPS:
        questions.extend([
            #TODO: make_numeric
        ])

    # Multiple choice questions
    if 'codeschool.questions.multiple_choice' in settings.INSTALLED_APPS:
        questions.extend([
            #TODO: make_multiple_choice
        ])

    # Form questions
    if 'codeschool.questions.form' in settings.INSTALLED_APPS:
        questions.extend([
            #TODO: make_form
        ])

    # Form questions
    if 'codeschool.questions.free_text' in settings.INSTALLED_APPS:
        questions.extend([
            #TODO: make_form
        ])

    return questions


def make_hello_world_submissions(question, user):
    submit = question.submit
    return [
        submit(user,
               source='print "hello world!"',
               language='python'),
        submit(user,
               source='print("hello world!")',
               language='python')
    ]
