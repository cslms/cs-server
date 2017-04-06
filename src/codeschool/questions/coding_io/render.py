from html import escape

from django.utils.translation import ugettext as _
from jinja2 import Markup

from bricks.helpers import render
from iospec import In, Out, IoSpec, TestCase
from iospec.feedback import Feedback


@render.register(In)
def _(x):
    data = escape(x, False)
    return Markup(
        '<span class="iospec-atom iospec-atom--in">%s</span><br>\n' % data)


@render.register(Out)
def _(x):
    data = escape(x, False)
    return Markup(
        '<span class="iospec-atom iospec-atom--out">%s</span>' % data)


@render.register(TestCase)
def _(x):
    if len(x) != 0:
        data = ''.join(map(render, x))
        return Markup(
            '<div class="iospec-testcase"><code>%s</code></div>' % data)
    else:
        data = escape(_('empty'))
        return Markup(
            '<div class="iospec-testcase iospec-testcase--empty">'
            '<code>-- %s --</code></div>' % data)


@render.register(IoSpec)
def _(x):
    data = '<br>\n'.join(map(render, x))
    return Markup(
        '<div class="iospec">%s</div>' % data)


render.register_template(Feedback, 'render/iospec/feedback.jinja2')
