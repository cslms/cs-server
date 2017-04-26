from django.template.context_processors import static
from django.utils.translation import ugettext as _

from bricks.components.tags import a
from bricks.tags import nav, a, p, ul, li, div, img


def navsection(title, links, href=None):
    """
    Creates a navsection element.

    Args:
        title: Title of the nav section.
        links: a list of links for this section.
        href: the optional link for the title element
    """

    title_cls = 'cs-nav__block-title'
    if href:
        title = a(class_=title_cls, href=href)[title]
    else:
        title = p(class_=title_cls)[title]
    return nav(class_='cs-nav__block')[
        title,
        ul(class_='cs-nav__block-items')[[
            li(elem) for elem in links
        ]],
    ]


def navbar(sections, class_=('cs-stripes-layout__sidebar',)):
    """
    Construct a navbar from a list of nav sections.
    """

    return div(class_=('cs-nav',) + tuple(class_))[
        div(sections),
        img(class_='cs-nav__dingbat', src='/static/img/dingbat.svg')
    ]


def navbar_page_admin(page, user, links=()):
    """
    Return a list of links for administrative tasks.

    The default list includes just an edit page. It can be supplemented with
    additional links.
    """
    pk = page.pk

    return navsection(_('Settings'), (
        a('Edit', href='/admin/pages/%s/edit/' % pk),
    ) + tuple(links))