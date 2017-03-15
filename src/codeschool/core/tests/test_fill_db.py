import os

import model_reference
import pytest
from iospec import IoSpec

import codeschool.questions.coding_io
from codeschool.auth.factories import make_yoda_teacher, make_teachers, \
    make_students, make_joe_user
from codeschool.conftest import model_fixture
from codeschool.lms.activities.factories import make_basic_activities
from codeschool.lms.courses.factories import make_cs101_course
from codeschool.questions.coding_io.models import CodingIoQuestion


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
    questions = [
        make_hello_world_question(basic),
        make_question_from_markio_example('simple.md', basic),
        make_question_from_markio_example('fibonacci.md', loops)
    ]
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


#
# Tests
#
joe_user = model_fixture(make_joe_user)
yoda_teacher = model_fixture(make_yoda_teacher)


@pytest.fixture
def root(db):
    return model_reference.load('root-page')


@pytest.fixture
def hidden_root(db):
    return model_reference.load('hidden-root')


@pytest.fixture
def hello_world_question(root):
    return make_hello_world_question(root)


def test_hello_world_submissions(hello_world_question, joe_user):
    sub1, sub2 = make_hello_world_submissions(hello_world_question, joe_user)


def test_create_yoda(db):
    yoda = make_yoda_teacher()
    assert yoda.profile
    assert yoda.profile.age == 900


def test_create_teachers(db):
    teachers = make_teachers()


def test_create_students(db):
    students = make_students(5)


def test_create_course(db, yoda_teacher):
    course = make_cs101_course(yoda_teacher)


def test_create_standard_activities(db):
    make_basic_activities()


def test_create_basic_coding_io_questions(db):
    parent = model_reference.load('rogue-root')
    make_hello_world_question(parent)
    make_question_from_markio_example('simple.md', parent)


def test_basic_coding_io_can_expand_tests(hello_world_question):
    question = hello_world_question
    pre = question.get_expanded_pre_tests()
    post = question.get_expand_post_tests()
    assert isinstance(pre, IoSpec)
    assert pre == post


def test_consecutive_submissions_recycle(db, hello_world_question, joe_user):
    qst = hello_world_question
    user = joe_user
    sub1 = qst.submit(user, source='print("hello")', language='python')
    sub2 = qst.submit(user, source='print("hello")', language='python')
    assert sub1.id == sub2.id
    assert sub2.num_recycles == 1


def test_can_send_submission_and_autograde(db, hello_world_question, joe_user):
    qst = hello_world_question
    user = joe_user
    sub1 = qst.submit(user, source='print("hello")', language='python')
    feedback = sub1.autograde()
    assert feedback.given_grade == 0
