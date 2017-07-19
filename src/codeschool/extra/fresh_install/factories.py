from logging import getLogger

from django.apps import apps

from codeschool.core.users.models import Profile

log = getLogger('codeschool.fresh_install')


def make_example_questions(parent):
    basic = parent.get_children().get(slug='basic')
    loops = parent.get_children().get(slug='loops')
    questions = []

    # Numeric questions
    if apps.is_installed('codeschool.questions.numeric'):
        # from codeschool.questions.numeric.factories import \
        #     make_numeric_question_42, make_numeric_question_pi

        questions.extend([
            # TODO: numeric question factories
            # make_numeric_question_42(basic),
            # make_numeric_question_pi(basic),
        ])

    # Coding Io questions
    if apps.is_installed('codeschool.questions.coding_io'):
        # from codeschool.questions.coding_io.factories import \
        #     make_question_from_markio_example, make_hello_world_question

        questions.extend([
            # TODO: coding io factories
            # make_hello_world_question(basic),
            # make_question_from_markio_example('simple.md', basic),
            # make_question_from_markio_example('fibonacci.md', loops)
        ])

    # Multiple choice questions
    if apps.is_installed('codeschool.questions.multiple_choice'):
        questions.extend([
            # TODO: make_multiple_choice
        ])

    # Form questions
    if apps.is_installed('codeschool.questions.form'):
        questions.extend([
            # TODO: make_form
        ])

    # Form questions
    if apps.is_installed('codeschool.questions.free_text'):
        questions.extend([
            # TODO: make_form
        ])

    return questions


def maurice_moss_profile(profile: Profile):
    log.info('Moss is the sysadmin!')
    profile.date_or_birth = (1982, 1, 6)
    profile.gender = profile.GENDER_MALE
    profile.website = 'https://www.reynholm.co.uk/~moss/'
    profile.about_me = (
        "Hi everyone and welcome to my web page. "
        "My name is Maurice Moss, my friends call me Moss. "
        "I'm a single I.T. guy from London, I'm in my 30's, "
        "I live with my mother, and I work for Reynholm Industries."
    )
    profile.phone = '+44 20 7946 3108 x3171'  # taken from facebook page
    profile.save()
