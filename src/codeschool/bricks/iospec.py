"""
Iospec renderers.
"""

from django.utils.translation import ugettext as _

from bricks.components.html5_tags import span
from bricks.html5 import div, br, code
from codeschool.bricks.utils import with_class, tag_join
from iospec import In

EMPTY = _('empty')


@with_class('iospec')
def iospec_to_html(iospec, **kwargs):
    """
    Renders IoSpec object as bricks HTML tags.
    """

    return \
        div(**kwargs)[
            tag_join(map(testcase_to_html, iospec)),
        ]


@with_class('iospec-testcase')
def testcase_to_html(testcase, **kwargs):
    if len(testcase) == 0:
        return \
            div(**with_class(kwargs, 'iospec-testcase--empty'))[
                code('-- %s --' % str(EMPTY))
            ]
    return \
        div(**kwargs)[
            code()[
                [atom_to_html(x) for x in testcase]
            ]
        ]


def atom_to_html(atom):
    class_ = ['iospec-atom', 'iospec-atom--%s' % type(atom).__name__.lower()]
    tag = span(str(atom), class_=class_)
    if isinstance(atom, In):
        return [tag, br()]
    return tag
