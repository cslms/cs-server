from .models import Question


#TODO: make
#@Question.register_route(r'^submit-response.api/$', name='submit-ajax')
def ajax_submission_view(client, page, **kwargs):
    return page.serve_ajax_submission(client, **kwargs)


@Question.register_route(r'^submissions/$', name='list-submissions')
def list_submissions_view(request, page, *args, **kwargs):
    raise NotImplementedError


@Question.register_route(r'^statistics/$', name='statistics')
def statistics_page_view(request, page, *args, **kwargs):
    raise NotImplementedError


@Question.register_route(r'^debug/$', name='debug')
def debug_page_view(request, page, *args, **kwargs):
    raise NotImplementedError
