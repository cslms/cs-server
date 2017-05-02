from functools import singledispatch

from django.utils.translation import ugettext as _

from bricks.contrib import mdl
from bricks.helpers import join_classes
from bricks.html5 import h3, dl, dt, dd, span, div
from codeschool.components.utils import with_class, title
from codeschool.lms.activities.models import Submission


@title.register(Submission)
def __(x):
    return x.get_feedback_title()


@with_class('cs-submission')
def submission(sub, hidden=True, **kwargs):
    """
    Display a submission object.
    """
    return \
        mdl.div(shadow=4, **kwargs)[
            submission_title(sub),
            submission_body(sub, hidden=hidden),
        ]


def submission_title(sub):
    return \
        h3(class_='cs-submission__title')[
            span(title(sub)),
            span(class_="cs-submission__title-handle",
                 onclick="expandSubmission(this.parentNode.parentNode)")[
                mdl.icon('menu'),
            ],
        ],


@singledispatch
def submission_body(sub, hidden=True):
    class_ = join_classes('cs-submission__content', hidden and 'hidden')
    grade = str(int(sub.final_grade_pc or 0)
                if sub.has_feedback else _('Not given'))

    # Collect submission data
    sub_data_title = h3(_('Submission data'), class_="banner")
    sub_data = submission_data(sub)
    sub_data = \
        sub_data and \
        div('cs-submission__data')[
            submission_title,
            sub_data,
        ]

    return \
        div(class_=class_)[
            div(class_='cs-submission__description')[
                str(sub),

            ],

            div(class_='cs-submission__detail')[
                h3(_('Details'), class_='banner'),
                dl()[
                    dt(_('Grade')),
                    dd(grade),
                    dt(_('Date of submission')),
                    dd(str(sub.created)),
                ],
            ],

            sub_data,
        ]


@singledispatch
def submission_data(submission):
    return None


submission_script = """
function expandSubmission(obj) {
    var expandable = $(obj).find('.cs-submission__content');
    if (expandable.length && expandable[0].classList.contains('hidden')) {
        expandable.removeClass('hidden').hide().show(200);
    } else {
        expandable.hide(200);
        window.setTimeout(function () {
            expandable.addClass('hidden')
        }, 200);
    }
}
"""
