from html import escape

from django.utils.translation import ugettext as _
from jinja2 import Markup

from bricks.helpers import render
from iospec import In, Out, IoSpec, TestCase
from iospec.feedback import Feedback


@render.register(In)
def _(x, request=None):
    data = escape(x, False)
    return Markup(
        '<span class="iospec-atom iospec-atom--in">%s</span><br>\n' % data)


@render.register(Out)
def _(x, request=None):
    data = escape(x, False)
    return Markup(
        '<span class="iospec-atom iospec-atom--out">%s</span>' % data)


@render.register(TestCase)
def _(x, request=None):
    if len(x) != 0:
        data = ''.join(render(e, request=request) for e in x)
        return Markup(
            '<div class="iospec-testcase"><code>%s</code></div>' % data)
    else:
        data = escape(_('empty'))
        return Markup(
            '<div class="iospec-testcase iospec-testcase--empty">'
            '<code>-- %s --</code></div>' % data)


@render.register(IoSpec)
def _(x, request=None):
    data = '<br>\n'.join(render(e, request=request) for e in x)
    return Markup(
        '<div class="iospec">%s</div>' % data)


render.register_template(Feedback, 'render/iospec/feedback.jinja2')
