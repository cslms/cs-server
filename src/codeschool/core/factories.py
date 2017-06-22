from mommys_boy import DjangoModelFactory, LazyAttributeSequence

from codeschool import settings
from codeschool.core import models


class ProgrammingLanguageFactory(DjangoModelFactory):

    class Meta:
        model = models.ProgrammingLanguage

    ref = LazyAttributeSequence(lambda x: 'lang%s' % x)
    name = LazyAttributeSequence(lambda x: 'Lang-%s' % x)


def make_example_questions(parent):
    basic = parent.get_children().get(slug='basic')
    loops = parent.get_children().get(slug='loops')
    questions = []

    # Numeric questions
    if 'codeschool.questions.numeric' in settings.INSTALLED_APPS:
        from codeschool.questions.numeric.factories import \
            make_numeric_question_42, make_numeric_question_pi

        questions.extend([
            make_numeric_question_42(basic),
            make_numeric_question_pi(basic),
        ])

    # Coding Io questions
    if 'codeschool.questions.coding_io' in settings.INSTALLED_APPS:
        from codeschool.questions.coding_io.factories import \
            make_question_from_markio_example, make_hello_world_question

        questions.extend([
            make_hello_world_question(basic),
            make_question_from_markio_example('simple.md', basic),
            make_question_from_markio_example('fibonacci.md', loops)
        ])

    # Multiple choice questions
    if 'codeschool.questions.multiple_choice' in settings.INSTALLED_APPS:
        questions.extend([
            # TODO: make_multiple_choice
        ])

    # Form questions
    if 'codeschool.questions.form' in settings.INSTALLED_APPS:
        questions.extend([
            # TODO: make_form
        ])

    # Form questions
    if 'codeschool.questions.free_text' in settings.INSTALLED_APPS:
        questions.extend([
            # TODO: make_form
        ])

    return questions
