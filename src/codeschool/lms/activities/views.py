import model_reference
from django.http import HttpResponse, Http404
from django.shortcuts import render

from codeschool.lms.activities.bricks import submission_list
from .models import Activity


def main_question_list(request):
    page = model_reference.load('main-question-list')
    return page.serve(request)


#
# Detail page
#
@Activity.register_route(r'^$', login_required=True)
def index(request, page, *args, **kwargs):
    context = page.get_context(request)
    template = page.get_template(request)
    return render(request, template, context)


#
# Activity sub-pages
#
@Activity.register_route(r'^submissions/$', login_required=True)
def list_submissions(request, page, *args, **kwargs):
    progress = page.progress_set.for_user(request.user)
    submissions = progress.submissions \
        .all() \
        .order_by('-created')

    ctx = {
        'page': page,
        'content_body': submission_list(submissions, progress),
        'navbar': page.get_navbar(request.user),
    }
    return render(request, 'page.jinja2', ctx)


@Activity.register_route(r'^csv/$', perms='activities.view_submission_stats')
def submissions_as_csv(request, page, *args, **kwargs):
    progress_manager = page.progress_class.objects
    csv = progress_manager.gradebook_csv(page)
    response = HttpResponse(csv, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="grades.csv"'
    return response
