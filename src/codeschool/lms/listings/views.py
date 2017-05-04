from django.shortcuts import render
from django.utils.translation import ugettext as _

from codeschool.bricks import card_container
from codeschool.lms.activities.bricks import activity_list_navbar
from codeschool.lms.listings.bricks import empty_card, card
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
