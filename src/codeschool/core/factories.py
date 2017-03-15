from mommys_boy import DjangoModelFactory, LazyAttributeSequence
from codeschool.factories import *
from codeschool.core import models


#
# File formats
#
class ProgrammingLanguageFactory(DjangoModelFactory):
    class Meta:
        model = models.ProgrammingLanguage

    ref = LazyAttributeSequence(lambda x: 'lang%s' % x)
    name = LazyAttributeSequence(lambda x: 'Lang-%s' % x)


# #
# # Activities
# #
#
# #
# # Courses
# #
# class FacultyFactory(factory.DjangoModelFactory):
#     class Meta:
#         model = models.Faculty
#
#     title = factory.LazyAttribute(lambda x: fake.word())
#     short_description = factory.LazyAttribute(lambda x: fake.sentence())
#
#
# class DisciplineFactory(factory.DjangoModelFactory):
#     class Meta:
#         model = models.Discipline
#
#     name = factory.LazyAttribute(lambda x: fake.word())
#     short_description = factory.LazyAttribute(lambda x: fake.sentence())
#     long_description = factory.LazyAttribute(lambda x: fake.text())
#     faculty = factory.SubFactory(FacultyFactory)
#
#
# class CourseFactory(factory.DjangoModelFactory):
#     class Meta:
#         model = models.Course
#
#     discipline = factory.SubFactory(DisciplineFactory)
#     teacher = factory.SubFactory(UserFactory)
#     is_active = True
#
#     @factory.post_generation
#     def num_students(self, create, extracted, **kwargs):
#         if create and extracted:
#             num_students = extracted
#             for _ in range(num_students):
#                 user = UserFactory.create()
#                 self.register_student(user)
#
#
# class UserWithCourseFactory(UserFactory):
#     course = factory.RelatedFactory(CourseFactory, 'enrolled_courses')
#
#
# # Clean namespace
# del factory