from codeschool.accounts.factories import make_yoda_teacher, make_students
from codeschool.factories import make_page
from codeschool.lms.courses.models import Course


def make_cs101_discipline():
    return make_page(
        'courses.Discipline',
        name='Programming 101',
        slug='cs101',
        description=(
            'Introductory programming course. Teachers basic programming '
            'concepts and enable students to make small software projects.'
        ),
        syllabus=(
            '<ul>'
            '<li>Variables and functions</li>'
            '<li>Conditionals and control loops</li>'
            '<li>Data structures</li>'
            '<li>Algorithms</li>'
            '</ul>'
        )
    )


def make_cs101_course(teacher=None, discipline=None, students=None):
    course = make_page(
        'courses.Course',
        root='course-list',
        title='Programming 101',
        slug='cs101',
        teacher=teacher or make_yoda_teacher(),
        discipline=discipline or make_cs101_discipline(),
        activities_template='programming-beginner',
    )
    students = make_students(5) if students is None else students
    for student in students:
        course.enroll_student(student)
    return course


def make_example_courses(students=None):
    cs101 = make_cs101_course(students=students)
    course_list = [cs101]
    return Course.objects.filter(id__in=[course.id for course in course_list])
