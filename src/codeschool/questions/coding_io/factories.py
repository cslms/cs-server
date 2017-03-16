import os

import model_reference

import codeschool.questions
from codeschool.questions.coding_io.models import CodingIoQuestion

example_path = os.path.join(os.path.dirname(__file__), 'examples')


def question_from_file(path, parent=None):
    """
    Load question from markio file
    """

    return CodingIoQuestion.import_markio_from_path(path, parent)


def question_from_example(name, parent=None):
    """
    Load question from markio file in examples.
    """

    path = os.path.join(example_path, name + '.md')
    return question_from_file(path, parent)


def source_from_example(name):
    """
    Return the source code for the example file.
    """

    path = os.path.join(example_path, name)
    with open(path) as F:
        data = F.read()
    return data


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
