from django.utils.translation import ugettext_lazy as _

from bricks.html5 import p, div, pre, h3, h4

CONGRATULATIONS = _('Congratulations! Your answer is correct!')


def feedback(feedback):
    raise NotImplementedError

    if feedback.is_correct:
        return \
            div(class_='cs-feedback')[
                p(CONGRATULATIONS, class_='cs-feedback__congratulations')
            ]
    else:
        with div(class_='cs-feedback') as root:
            root << h3(_(feedback.title), class_="iospec-feedback-title")

            if feedback.is_build_error:
                root << simple_error_message(feedback, _(
                    'An error occured while preparing your program for '
                    'execution. Please check the source code syntax.'
                ))

            elif feedback.is_timeout_error:
                root << p(_(
                    'Program execution was cancelled because it was taking '
                    'too long.'
                ))

            elif feedback.is_runtime_error:
                root << simple_error_message(feedback, _(
                    'An error occurred during program execution.'
                ))

            else:  # wrong answer/presentation
                root << feedback_wrong_answer(feedback)

        return root


def feedback_wrong_answer(feedback):
    return [
        div()[
            h4(_('Your response')),
            html(feedback.testcase),
        ],
        div()[
            h4(_('Expected answer')),
            html(feedback.answer_key),
        ]
    ]


def simple_error_message(feedback, msg):
    return [
        p(msg),
        h4(_('Error message')),
        pre(feedback.get_error_message()),
    ]
