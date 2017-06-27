from django.apps import apps


def make_example_questions(parent):
    basic = parent.get_children().get(slug='basic')
    loops = parent.get_children().get(slug='loops')
    questions = []

    # Numeric questions
    if apps.is_installed('codeschool.questions.numeric'):
        from codeschool.questions.numeric.factories import \
            make_numeric_question_42, make_numeric_question_pi

        questions.extend([
            make_numeric_question_42(basic),
            make_numeric_question_pi(basic),
        ])

    # Coding Io questions
    if apps.is_installed('codeschool.questions.coding_io'):
        from codeschool.questions.coding_io.factories import \
            make_question_from_markio_example, make_hello_world_question

        questions.extend([
            make_hello_world_question(basic),
            make_question_from_markio_example('simple.md', basic),
            make_question_from_markio_example('fibonacci.md', loops)
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
