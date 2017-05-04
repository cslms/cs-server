import model_reference
from django.http import HttpResponse
from django.shortcuts import render

from codeschool.lms.activities.bricks import submission_list
from .models import Activity


def main_question_list(request):
    page = model_reference.load('main-question-list')
    return page.serve(request)


#
# Activity sub-pages
#
@Activity.register_route(r'^submissions/$',
                         name='activity-list-submissions',
                         login_required=True)
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


@Activity.register_route(r'^csv/$',
                         name='activity-progress-csv',
                         perms='activities.view_submission_stats')
def submissions_as_csv(request, page, *args, **kwargs):
    progress_manager = page.progress_class.objects
    csv = progress_manager.gradebook_csv(page)
    response = HttpResponse(csv, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="grades.csv"'
    return response
