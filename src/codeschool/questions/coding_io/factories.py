import os

from django.test import RequestFactory

import codeschool.questions
from codeschool.core.models import get_wagtail_root_page
from codeschool.questions.coding_io.loaders import import_markio_from_path
from codeschool.questions.coding_io.models import CodingIoQuestion

example_path = os.path.join(os.path.dirname(__file__), 'examples')


def question_from_file(path, parent=None) -> CodingIoQuestion:
    """
    Load question from markio file
    """

    parent = parent or get_wagtail_root_page()
    return import_markio_from_path(path, parent)


def question_from_example(name, parent=None) -> CodingIoQuestion:
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
    parent = parent or get_wagtail_root_page()
    question = import_markio_from_path(path, parent)
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
    parent = parent or get_wagtail_root_page()
    parent.add_child(instance=question)
    return question


def make_hello_world_submissions(question, user):
    submit = question.submit
    request = RequestFactory().get('/')
    request.user = user
    sub1 = submit(request,
                  source='print "hello world!"',
                  language='python')
    sub2 = submit(request,
                  source='print("hello world!")',
                  language='python')
    return [sub1, sub2]
