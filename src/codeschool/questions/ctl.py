from traceback import print_tb

import markio
import sys
from wagtail.wagtailcore.models import Page

from codeschool.questions.coding_io.models import CodingIoQuestion


def push_question(filename, contents, parent, user):
    """
    Saves new question with the given filename and contents to the database.

    Args:
        filename:
            name of the question source. Usually we are only interested in
            the file extension.
        contents:
            A string (or bytes) with the file content.
        parent (str):
            A hint for the desired parent page for the question.
        user:
            User making the request.

    Returns:
        The the submitted question.
    """

    parent = find_parent(parent)
    check_publish_credentials(user, parent)

    if not filename.endswith('.md'):
        raise ValueError('not a valid filename')
    question = markio.parse_markio(contents)
    return CodingIoQuestion.import_markio(question, parent)


def push_question_json(filename, contents, parent, user):
    """
    Like push_question(), but wraps the result in a JSON object.
    """

    try:
        question = push_question(filename, contents, parent, user)
    except Exception as ex:
        print_tb(ex.__traceback__)
        return {'error': str(ex)}
    else:
        return {'result': question.get_absolute_url()}



def check_publish_credentials(user, parent):
    """
    Raise a PermissionError if user cannot publish under the given parent page.
    """

    if not user.is_superuser:
        raise PermissionError
