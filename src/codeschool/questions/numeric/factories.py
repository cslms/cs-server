import math
import model_reference

from codeschool.questions.numeric.models import NumericQuestion


def make_numeric_question_42(parent=None, commit=True):
    question = NumericQuestion(
        title='The Answer',
        body=[
            ('markdown',
             'What is The Answer to the Ultimate Question of Life, The '
             'Universe, and Everything?'),
        ],
        correct_answer=42,
    )
    if commit:
        parent = parent or model_reference.load('root-page')
        parent.add_child(instance=question)
    else:
        question.path = '0002'
        question.depth = 1
    return question


def make_numeric_question_pi(parent=None):
    question = NumericQuestion(
        title='Pie',
        body=[
            ('markdown',
             'What is the value of Pi?'),
        ],
        correct_answer=math.pi,
        tolerance=0.01,
    )
    parent = parent or model_reference.load('root-page')
    parent.add_child(instance=question)
    return question
