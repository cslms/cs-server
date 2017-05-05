from django.utils.translation import ugettext as _

from codeschool.bricks import simple_card


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
