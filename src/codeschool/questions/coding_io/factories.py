import os

from codeschool.questions.coding_io.models import CodingIoQuestion


def question_from_file(path, parent=None):
    """
    Load question from markio file
    """

    return CodingIoQuestion.import_markio_from_path(path, parent)


def question_from_example(name, parent=None):
    """
    Load question from markio file in examples.
    """

    examples = os.path.join(os.path.dirname(__file__), 'examples')
    path = os.path.join(examples, name + '.md')
    return question_from_file(path, parent)


def source_from_example(name):
    """
    Return the source code for the example file.
    """

    examples = os.path.join(os.path.dirname(__file__), 'examples')
    path = os.path.join(examples, name)
    with open(path) as F:
        data = F.read()
    return data
