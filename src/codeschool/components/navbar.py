from django.template.context_processors import static
from django.utils.translation import ugettext as _

from bricks.components.html5_tags import a
from bricks.html5 import nav, a, p, ul, li, div, img


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


def navsection_page_admin(page, user, links=()):
    """
    Return a list of links for administrative tasks.

    The default list includes just an edit page. It can be supplemented with
    additional links.
    """
    pk = page.pk

    return navsection(_('Settings'), (
        a('Edit', href='/admin/pages/%s/edit/' % pk),
    ) + tuple(links))


def navbar(sections=None, class_=('cs-stripes-layout__sidebar',),
           admin=False, admin_links=(), admin_perms=None, user=None, page=None):
    """
    Construct a navbar from a list of nav sections.

    Args:
        sections:
            List of sections.
        class:
            Optional class to root navbar div
        user:
            User making request.
        page:
            Page associated with request. Necessary for
        admin:
            If True or a callable of admin(page, user), it builds an admin
            section for allowed users.
        admin_perms:
            The permissions required to use the admin.
        admin_links:
            Any extra links to be included in the default admin section.
    """

    sections = list(sections or [])

    # Insert admin sections
    if admin:
        page_args = () if page is None else (page,)
        if admin_perms and user.has_perms(admin_perms, *page_args) or \
                user.is_superuser:
            if callable(admin):
                admin = admin(page, user)
            else:
                admin = navsection_page_admin(page, user, admin_links)
            sections.insert(0, admin)

    return div(class_=('cs-nav',) + tuple(class_))[
        div(sections),
        img(class_='cs-nav__dingbat', src='/static/img/dingbat.svg')
    ]
