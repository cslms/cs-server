import model_reference

from codeschool import models
from codeschool.core.config import global_data_store
from codeschool.core.users.factories import make_joe_user
from codeschool.lms.activities.factories import make_basic_activities
from codeschool.lms.classrooms.factories import make_example_course_list


def fill_data(data, user):
    if data.get('joe_user', False):
        fill_joe_user()

        # TODO: populate database
        # if data.get('basic_activities', False):
        #     fill_basic_activities()
        # if data.get('example_questions', False):
        #     fill_example_questions(user)
        # if data.get('example_courses', False):
        #     fill_example_courses()
        # if data.get('populate_courses', False):
        #     fill_courses_with_users()
        # if data.get('example_submissions', False):
        #     fill_example_submissions()


def fill_joe_user():
    joe = make_joe_user()
    global_data_store['joe-user-id'] = joe.id
    return joe


def fill_basic_activities():
    if 'main-question-list' not in global_data_store:
        global_data_store['main-question-list'] = 'basic'
        make_basic_activities()


def fill_example_questions(user):
    from .factories import make_example_questions

    if not global_data_store.get('example-questions', False):
        global_data_store['example-questions'] = True
        activities = model_reference.load('main-question-list')
        questions = make_example_questions(activities)
        for i in range(1, min(2, len(questions))):
            questions[i].owner = user
            questions[i].save()


def fill_example_courses():
    if not global_data_store.get('example-courses', False):
        global_data_store['example-courses'] = True
        cs101, *other_courses = make_example_course_list()
        cs101.teacher = models.User.objects.get(
            id=global_data_store['admin-user-id'])
        cs101.save()


def fill_courses_with_users():
    from codeschool.lms.classrooms.models import Classroom
    from codeschool.core.users.factories import make_teachers, make_joe_user, \
        make_mr_robot

    if not global_data_store.get('courses-populated', False):
        user = models.User.objects.get(id=global_data_store['admin-user-id'])
        global_data_store['courses-populated'] = True
        teachers = [user]
        teachers.extend(make_teachers())
        common = [make_mr_robot(), make_joe_user()]

        for teacher, course in zip(teachers, Classroom.objects.all()):
            from codeschool.users.factories import make_students
            for student in list(make_students(3)) + common:
                course.enroll_student(student)
            course.teacher = teacher
            course.save()


def fill_example_submissions():
    if not global_data_store.get('example-submissions'):
        global_data_store['example-submissions'] = True

        # TODO: implement this
        # make_example_submissions()
