from django.utils.translation import ugettext as _

from bricks.contrib import mdl
from bricks.helpers import hyperlink, markdown
from bricks.html5 import img, dl, dd, dt, a
from codeschool import bricks

# Mugshot
mugshot = lambda profile: \
    img(class_='mugshot', src=profile.get_mugshot_url(), alt=_('Your mugshot'))


def profile(profile: 'accounts.Profile', **kwargs):
    """
    Base profile brick for a given user profile.
    """
    return \
        mdl.div(shadow=4, class_='mdl-grid', **kwargs)[
            mdl.div(class_='mdl-cell mdl-cell--3-col')[
                mugshot(profile)
            ],
            mdl.div(class_='mdl-cell mdl-cell--9-col')[
                profile_description(profile)
            ]
        ]


def profile_description(profile, **kwargs):
    with dl(class_='user-details', **kwargs) as tag:
        fullname = profile.user.get_full_name()
        if fullname:
            tag << [dt(_('Name')), dd(fullname)]
        if profile.user.email:
            tag << [dt(_('E-mail')), dd(profile.email)]
        if profile.age:
            tag << [dt(_('Age')), dd(str(profile.age))]
        if profile.website:
            url = profile.website
            tag << [dt(_('Website')), dd(a(url, href=url))]
        if profile.about_me:
            tag << [dt(_('About me')), dd(markdown(profile.about_me))]
    return tag


def navbar(user, **kwargs):
    sections = [
        bricks.navsection(
            _('Profile'), map(hyperlink, [
                _('Edit </profile/edit/>'),
                _('Change password </profile/change-password/>'),
            ]))
    ]
    return bricks.navbar(sections)
