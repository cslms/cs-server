from rest_framework import viewsets

from . import models
from . import serlializers
from .models import Question


#
# API end points
#
class QuestionViewSet(viewsets.ModelViewSet):
    """
    Represent the generic fields of questions.

    Specific fields are shown in specific sub-urls.
    """

    # queryset = Page.objects.all()
    serializer_class = serlializers.QuestionSerializer


#
# Question sub-pages
#
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
