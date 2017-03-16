from html import escape

from django.utils.translation import ugettext as _
from iospec.feedback import Feedback
from jinja2 import Markup

from codeschool.questions.coding_io.models import CodingIoFeedback
from iospec import In, Out, IoSpec, TestCase
from pyml.helpers import render


@render.register(CodingIoFeedback)
def _(x, **kwargs):
    if x.get_feedback:
        return render(x.get_feedback, **kwargs)
    else:
        return _('Incomplete get_feedback')


@render.register(In)
def _(x):
    return Markup(
        '<span class="iospec-atom iospec-atom--in">%s</span><br>\n' % escape(x,
                                                                             False))


@render.register(Out)
def _(x):
    return Markup(
        '<span class="iospec-atom iospec-atom--out">%s</span>' % escape(x,
                                                                        False))


@render.register(TestCase)
def _(x):
    if len(x) != 0:
        data = ''.join(map(render, x))
        return Markup(
            '<code class="iospec-testcase">%s</code>' % data)
    else:
        data = escape(_('empty'))
        return Markup(
            '<code class="iospec-testcase iospec-testcase--empty">'
            '-- %s --</code>' % data)


@render.register(IoSpec)
def _(x):
    data = '<br>\n'.join(map(render, x))
    return Markup(
        '<div class="iospec">%s</div>' % data)


render.register_template(Feedback, 'render/iospec/get_feedback.jinja2')
