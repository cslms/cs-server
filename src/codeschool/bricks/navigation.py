from django.utils.translation import ugettext as _

from bricks.contrib import mdl
from bricks.helpers import join_classes
from bricks.html5 import nav, a, p, ul, li, div, img, link, span, script


#
# Navigation bar
#
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


#
# Foot component
#
def footer(class_=None, **kwargs):
    """
    Renders the default foot element.
    """

    class_ = join_classes('cs-foot', class_)
    return \
        div(class_=class_, **kwargs)[
            div(class_="cs-foot__copyright")[
                p([
                    'Copyright 2016 - ',
                    link('Codeschool <http://github.com/cslms/cs-server>')
                ]),
                p('Site gerenciado por Fábio M. Mendes na UnB/Gama.')
            ]
        ]


#
# Head element
#
def head(links=None, user=None, class_=None, **kwargs):
    """
    Renders the default head element.

    Args:
        links:
            A list of hyperlinks that enter the main navigation area.
        user:
            The user requesting the page. The user name is used to set the
            fab button icon.
    """

    fabletter = None
    if user and not user.is_anonymous:
        fabletter = user.first_name[0:1] or user.username[0]

    return \
        div(class_=join_classes('cs-head', class_), **kwargs)[
            _head_logo(),
            _head_nav(links, fabletter=fabletter),
            _head_script(),

        ]


def _head_logo():
    return \
        div(class_="cs-logo")[
            img(class_="cs-logo__img", src='/static/img/logo.svg')
        ]


def _head_nav(children=None, fabletter=None):
    return \
        nav(class_="cs-head__nav")[
            div(children, class_="cs-head__links"),
            mdl.button(class_='cs-head__fab', colored=True, fab=True,
                       id='cs-head--dropdown-trigger')[
                span(fabletter or '?', class_='dropdown-trigger')
            ],
            _head_menu(),
        ]


def _head_menu_link(name, link):
    return li(class_="mdl-menu__item")[a(name, href=link)],


def _head_menu():
    return \
        ul(class_="mdl-menu mdl-menu--bottom-left mdl-js-menu "
                  "mdl-js-ripple-effect", for_="cs-head--dropdown-trigger")[
            _head_menu_link(_('Profile'), '/auth/profile/'),
            _head_menu_link(_('Logout'), '/auth/logout/'),
        ]


def _head_script():
    return \
        script()[
            """
            $('.cs-head--links').click(function () {
                var nav = this;

                if (nav.style.display === 'none' || nav.style.display === '') {
                    nav.style.display = 'flex';
                } else {
                    nav.style.display = '';
                }
            });
            """
        ]
