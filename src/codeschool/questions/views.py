from django.shortcuts import render

from .models import Question


# TODO: make
# @Question.register_route(r'^submit-response.api/$', name='submit-ajax')
def ajax_submission_view(client, page, **kwargs):
    return page.serve_ajax_submission(client, **kwargs)


@Question.register_route(r'^submissions/$',
                         name='question-list-submissions',
                         login_required=True)
def list_submissions_view(request, page, *args, **kwargs):
    template = page.get_template(request, basename='submissions')
    context = page.get_context(request)
    submissions = page.progress_set.for_user(request.user).submissions.all()
    context['submissions'] = submissions
    return render(request, template, context)


@Question.register_route(r'^statistics/$',
                         name='question-statistics',
                         login_required=True)
def statistics_page_view(request, page, *args, **kwargs):
    raise NotImplementedError


@Question.register_route(r'^debug/$',
                         name='question-debug',
                         login_required=True)
def debug_page_view(request, page, *args, **kwargs):
    raise NotImplementedError
