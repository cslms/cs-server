from django.http import HttpResponse
from django.shortcuts import render
from django.utils.translation import ugettext as _
from rest_framework import viewsets
from rest_framework.decorators import detail_route

from codeschool.bricks import card_container
from . import serializers
from .bricks import empty_card, card, activity_list_navbar
from .models import ActivityList, ActivitySection


#
# API
#
class ActivitySectionViewSet(viewsets.ModelViewSet):
    """
    A list of activities.
    """

    queryset = ActivitySection.objects.all()
    serializer_class = serializers.ActivitySectionSerializer

    @detail_route(methods=['GET'])
    def csv(self, request, pk):
        obj = ActivitySection.objects.get(pk=pk)
        return HttpResponse(
            obj.grades_as_csv().encode(request.encoding or 'latin9'),
            content_type='text/plain',
        )


class ActivityListViewSet(viewsets.ModelViewSet):
    """
    A list of activities.
    """

    queryset = ActivityList.objects.all()
    serializer_class = serializers.ActivityListSerializer


#
# Page sub-urls
#
@ActivityList.register_route('^$', login_required=True)
def list_view(request, page):
    subpages = [obj.specific for obj in page.get_children()]
    cards = [card(x) for x in subpages] or empty_card()
    main = \
        card_container(
            cards,
            title=_('Activities'),
            description=_('List of activities'),
        )

    ctx = {
        'page': page,
        'main': main,
        'navbar': activity_list_navbar(page, request.user),
    }
    return render(request, 'base.jinja2', ctx)


@ActivitySection.register_route('^$', login_required=True)
def section_view(request, page):
    subpages = [obj.specific for obj in page.get_children()]
    cards = [card(x) for x in subpages] or empty_card()
    main = \
        card_container(
            cards,
            title=page.title,
            description=page.short_description,
        )

    ctx = {
        'page': page,
        'main': main,
        'navbar': activity_list_navbar(page, request.user),
    }
    return render(request, 'base.jinja2', ctx)


@ActivitySection.register_route('^grades.csv/$', login_required=True)
def section_view(request, page):
    response = HttpResponse('foo,bar,baz\n1,2,3')
    response['content_type'] = 'text/csv; charset=utf-8'
    return response
