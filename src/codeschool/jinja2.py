import collections
from functools import singledispatch
from logging import Logger

from django.contrib.staticfiles.storage import staticfiles_storage
from django.core.urlresolvers import reverse
from django.utils.html import escape
from django.utils.translation import ugettext, ungettext
from jinja2 import Environment, Markup, contextfilter, contextfunction, \
    is_undefined
from jinja2.runtime import Context
from pygments import highlight as pygments_highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import get_formatter_by_name
from pyml.components.data_components import Mapping
from pyml.helpers import render, hyperlink
from wagtail.wagtailcore.templatetags.wagtailcore_tags import richtext

jinja2_environment = None

log = Logger('codeschool.settings')


class CodeschoolContext(Context):
    """
    Inject context variables in a jinja2 context.
    """


class Hooks:
    """
    Extensible points to be used in templates.
    """

    def __init__(self):
        self._head_links = []


class GlobalConfig:
    """
    Expose configurations to templates.
    """

    def __getattr__(self, attr):
        if attr.isupper():
            from codeschool.settings import codeschool
            return getattr(codeschool, attr, None)


def markdown(text, *args, **kwargs):
    """
    Convert a string of markdown source to HTML.
    """

    from markdown import markdown
    return markdown(text, *args, **kwargs)


def highlight(code, lang='python'):
    """
    Highlights source in the given programming language.
    """

    formatter = get_formatter_by_name('html')
    lexer = get_lexer_by_name(lang)
    return Markup(pygments_highlight(code, lexer, formatter))


def icon(value):
    """
    Convert value to a material-icon icon tag.
    """
    if value is True:
        return '<i class="material-icons">done</i>'
    elif value is False:
        return '<i class="material-icons">error</i>'
    else:
        return '<i class="material-icons">%s</i>' % escape(value)


def breadcrumbs_from_request(request):
    parts = request.path.split()
    trail = []
    url = ''
    for part in parts:
        url = '%s/%s' % (url, part)
        title = part.title()
        trail.append(Markup('<a href="%s">%s</a>' % (url, title)))

    if len(trail) == 1:
        return []
    return trail[::-1]


def breadcrumbs_from_page(page):
    trail = []
    while page:
        url = page.get_absolute_url()
        title = escape(page.title)
        trail.append(Markup('<a href="%s">%s</a>' % (url, title)))
        page = page.get_parent()
    trail = trail[:-2]
    if len(trail) == 1:
        return []
    return trail[::-1]


@contextfilter
def breadcrumbs(ctx, page=None):
    """
    Return a list of breadcrumb links for the given page or request.
    """

    if is_undefined(page):
        page = ctx.get('page', None)
    if hasattr(page, 'breadcrumbs'):
        return page.breadcrumbs()
    elif page is None:
        return breadcrumbs_from_request(ctx['request'])
    elif isinstance(page, str):
        raise ValueError('cannot extract breadcrumbs from string')
    elif isinstance(page, collections.Sequence):
        return list(page)
    else:
        return breadcrumbs_from_page(page)


@contextfilter
def dl(ctx, object, *args, **kwargs):
    """
    Renders mapping-like object or list of 2-tuples as an HTML description list.
    """

    component = Mapping(object, *args, **kwargs)
    return Markup(component.render(ctx['request']))


@contextfunction
def make_nav_sections(ctx, obj=None):
    """
    Creates nav sections for page.
    """

    if obj:
        return obj.nav_sections(ctx['request'])
    if 'page' in ctx:
        return ctx['page'].nav_sections(ctx['request'])
    return []


@singledispatch
def finalize(obj):
    if obj is None:
        return ''
    return obj


def environment(**options):
    """
    Creates jinja2 environment during django initialization.
    """

    global jinja2_environment

    env = jinja2_environment = Environment(**options)

    # Globals
    env.globals.update(
        static=staticfiles_storage.url,
        url=reverse,
        hooks=Hooks(),
        cfg=GlobalConfig(),
        make_nav_sections=make_nav_sections,
    )

    # Filters
    env.filters.update(
        markdown=markdown,
        highlight=highlight,
        icon=icon,
        dl=dl,
        html=render,
        breadcrumbs=breadcrumbs,
        hyperlink=hyperlink,
        richtext=richtext,
    )

    # Finalizer
    env.finalize = finalize

    # Translations
    env.install_gettext_callables(ugettext, ungettext, newstyle=True)

    # Custom context
    env.context_class = CodeschoolContext

    log.info('jinja2 enviroment initialized')
    return env
