import model_reference

from codeschool.questions.text.models import TextQuestion


def make_text_questions(parent=None):
    question = TextQuestion(
        title='The Answer',
        body=[
            ('markdown',
             'What is The Answer to the Ultimate Question of Life, The '
             'Universe, and Everything?'),
        ],
        correct_answer='joÃo',
    )
    parent = parent or model_reference.load('root-page')
    parent.add_child(instance=question)
    return question


def make_text_questions_fuzzy(parent=None):
    question = TextQuestion(
        title='Pie',
        body=[
            ('markdown',
             'What is the value of Pi?'),
        ],
        correct_answer='ÁloMundo'
    )
    parent = parent or model_reference.load('root-page')
    parent.add_child(instance=question)
    return question
