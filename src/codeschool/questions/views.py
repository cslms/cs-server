from django.shortcuts import render

from .models import Question


# TODO: make
# @Question.register_route(r'^submit-response.api/$', name='submit-ajax')
def ajax_submission_view(client, page, **kwargs):
    return page.serve_ajax_submission(client, **kwargs)


@Question.register_route(r'^statistics/$',
                         name='question-statistics',
                         login_required=True)
def statistics_page(request, page, *args, **kwargs):
    raise NotImplementedError


@Question.register_route(r'^debug/$',
                         name='question-debug',
                         login_required=True)
def debug_page(request, page, *args, **kwargs):
    raise NotImplementedError
