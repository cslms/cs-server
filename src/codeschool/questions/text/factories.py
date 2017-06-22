import model_reference

from codeschool.questions.text.models import TextQuestion


def make_text_question(parent=None):
    question = TextQuestion(
        title='The textual answer for everything',
        body=[
            ('markdown',
             'What is bigger than the answer to the Ultimate Question of Life, The '
             'Universe, and Everything?'),
        ],
        correct_answer='Quarenta e três',
    )
    parent = parent or model_reference.load('root-page')
    parent.add_child(instance=question)
    return question


def make_regex_text_question(parent=None):
    question = TextQuestion(
        title='The E-mail',
        body=[
            ('markdown',
             'What is your e-mail?'),
        ],
        # E-mail regex
        correct_answer='(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)',
    )
    parent = parent or model_reference.load('root-page')
    parent.add_child(instance=question)
    return question
