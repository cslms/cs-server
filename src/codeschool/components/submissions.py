from functools import singledispatch

from bricks.contrib.mdl import div, span, icon
from bricks.helpers import join_classes
from bricks.html5 import h3, dl, dt, dd
from codeschool.lms.activities.models import Submission


@singledispatch
def title(obj):
    """
    Return a title string for object.
    """

    try:
        return obj.title
    except AttributeError:
        return str(obj)


@title.register(Submission)
def _(x):
    return x.get_feedback_title()


def submission(submission, class_=None):
    """
    Display a submission object.
    """

    class_ = join_classes(class_, 'cs-submission')
    return \
        div(class_=class_, shadow=4)[
            submission_title(submission),
            submission_body(submission),
        ]


@singledispatch
def submission_title(submission):
    return \
        h3(class_='cs-submission__title')[
            span(title(submission)),
            span(class_="cs-submission__title-handle",
                 onclick="expandSubmission(this.parentNode.parentNode)")[
                icon('menu'),
            ],
        ],


@singledispatch
def submission_body(submission, hidden=True):
    class_ = join_classes('cs-submission__content', hidden and 'hidden')
    grade = (int(submission.final_grade_pc)
             if submission.has_feedback else _('Not given'))

    # Collect submission data
    sub_data_title = h3(_('Submission data'), class_="banner")
    sub_data = submission_data(submission)
    sub_data = sub_data and [submission_title, sub_data]

    return \
        div(class_=class_)[
            str(submission),
            h3(_('Details'), class_='banner'),
            dl()[
                dt(_('Grade')),
                dd(grade),
                dt(_('Date of submission')),
                dd(submission.created),
            ],
            sub_data
        ]


@singledispatch
def submission_data(submission):
    return None


submission_script = """
function expandSubmission(obj) {
    var expandable = $(obj).find('.expandable');
    if (expandable[0].classList.contains('hidden')) {
        expandable.removeClass('hidden').hide().show(200);
    } else {
        expandable.hide(200);
        window.setTimeout(function () {
            expandable.addClass('hidden')
        }, 200);
    }
}
"""
