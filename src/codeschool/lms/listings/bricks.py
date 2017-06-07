from django.utils.translation import ugettext as _

from codeschool.bricks import simple_card, navbar, navsection
from bricks.html5 import a


def empty_card():
    return simple_card(
        _('Empty'),
        text=_('No section found'),
        icon='do_not_disturb',
        faded=True,
    )


def card(section):
    return simple_card(
        section.title,
        text=section.short_description,
        icon=getattr(section, 'material_icon', 'help'),
        href=section.slug
    )


def activity_list_navbar(page, user):
    if user.is_superuser:
        sections = [navsection(_('Resources'), [
            a(_('Student grades')  , href='grades.csv'),
        ])]
    else:
        sections = []

    return navbar(sections=sections, admin=True, \
                  admin_perms='activities.edit_activity',
                  user=user, page=page)


def activity_section_navbar(page, user):
    return navbar(admin=True, admin_perms='activities.edit_activity',
                  user=user, page=page)
