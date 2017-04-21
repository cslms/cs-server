import model_reference
from django.http import HttpResponse, Http404
from rules.contrib.views import permission_required

from .models import Activity, Progress


def main_question_list(request):
    page = model_reference.load('main-question-list')
    return page.serve(request)


@Activity.register_route(r'^csv/$',
                         name='activity-progress-csv',
                         perms='activities.view_submission_stats')
def list_submissions_view(request, page, *args, **kwargs):
    manager = Progress.objects  # FIXME: page.progress_class.objects?
    csv = manager.gradebook_csv(page)
    response = HttpResponse(csv, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="grades.csv"'
    return response
