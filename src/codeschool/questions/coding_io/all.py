from plagiarism.input import ask
from plagiarism.tasks import interactive_find_suspects
from plagiarism.text import dedent as _dedent

from codeschool import models
from .models import *


def get_page(query, model=models.Page):
    """
    Return page (or sub-class) from given query. This function tries to be
    smart.
    """

    if isinstance(query, str):
        query = query.rstrip('/')
        qs1 = model.objects.filter(url_path__endswith=query + '/')
        if qs1.count() == 1:
            return qs1.first()

        qs2 = model.objects.filter(url_path__contains=query)
        if qs2.count() == 1:
            return qs2.first()

        qs3 = model.objects.filter(slug=query.rpartition('/')[-1])
        if qs3.count() == 1:
            return qs3.first()

    raise NotImplementedError


def find_suspects(question=None, dedent=False, **kwargs):
    """
    Find suspicious submissions.
    """

    question = get_page(ask(question, input, 'Question: '), CodingIoQuestion)
    codes = CodingIoSubmission.objects \
        .for_activity(question) \
        .best_code_for_users()
    if dedent:
        codes = {k: _dedent(v) for k, v in codes.items()}
    interactive_find_suspects(codes, **kwargs)
