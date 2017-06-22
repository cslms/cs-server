"""
Simple view that render components as HTML.

This is available only when DEBUG=True.
"""
import model_reference
from django.shortcuts import render
from markupsafe import Markup

from bricks.components.html5_tags import h1, script
from bricks.contrib.mdl import div
from bricks.helpers import safe
from .cards import card_container, simple_card
from .iospec import iospec_to_html
from .navigation import navbar, navsection, navsection_page_admin


def tag_view(func):
    """
    Takes a function that return a tag and return a Django view.
    """

    title = func.__name__.rpartition('_')[0].title()

    def decorated(request):
        tag = func()
        return render_tag(request, title, tag)

    return decorated


def navbar_view(request):
    from codeschool.models import User

    user = User.objects.last()
    page = model_reference.load('root-page')

    sections = [navsection('Foo', ['link1', 'link2', 'link3']),
                navsection_page_admin(page, user=user)]
    navbar_elem = navbar(sections)

    return render_tag(request, 'Navbars', div()[
        div('Main content'),
    ], ctx={'navbar': navbar_elem})


@tag_view
def iospec_view():
    from iospec import parse

    iospec = parse(
        'name: <John>\n'
        'Hello John!\n'
    )
    return iospec_to_html(iospec)


@tag_view
def cards_view():
    card_list = [
        simple_card('Card title'),
        simple_card('Title', 'This is a simple description.'),
        simple_card('Fancy', 'Card with an icon and link.',
                    icon='code', href='./navbar'),
        simple_card('Faded', 'Disabled card.', faded=True),
    ]
    return \
        div()[
            h1('Container with title and aside'),
            card_container(
                title='Title',
                description='This is a small description on an aside',
                cards=card_list
            ),

            h1('Container without title'),
            card_container(card_list),

            h1('Cards inside a simple div'),
            div(card_list),
        ]


@tag_view
def submissions_view():
    from codeschool.questions.coding_io.models import CodingIoSubmission
    from codeschool.lms.activities.bricks import submission, submission_script

    sub1, sub2, sub3, sub4 = CodingIoSubmission.objects.order_by(
        '-created')[:4]

    return div()[
        submission(sub1, hidden=False),
        submission(sub2),
        submission(sub3),
        submission(sub4),
        submission_script,
    ]


@tag_view
def feedback_view(request):
    from codeschool.questions.coding_io.models import CodingIoFeedback

    feedbacks = CodingIoFeedback.objects.order_by('-created')[:10]

    return div()[
        [div(shadow=4, style='margin: 20px;')[fb] for fb in feedbacks]
    ]


def render_tag(request, title, tag, ctx=None):
    html = Markup(tag.render(request))
    ctx = dict(
        ctx or {},
        content_title=title,
        content_body=div(html, shadow=6, style='padding: 20px'),
    )
    return render(request, 'base.jinja2', ctx)
