from django.shortcuts import render
from django.utils.translation import ugettext as _
from django.http import HttpResponse

from codeschool.bricks import card_container
from .bricks import empty_card, card, activity_list_navbar
from .models import ActivityList, ActivitySection


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