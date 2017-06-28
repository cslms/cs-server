from django.utils.translation import ugettext as _

from bricks.components.html5_tags import a
from codeschool.bricks.navigation import navbar, navsection, \
    navsection_page_admin


def navsection_question_common(question, user):
    """
    Common sections:

    [link to page root]
        * Submissions
    """
    links = [
        a(_('Submissions'), href=question.get_absolute_url('submissions'))
    ]
    return navsection(question.title, links, href=question.get_absolute_url())


def navbar_question(question, user):
    sections = []

    if user.has_perm('activities.edit_activity'):
        sections.append(navsection_page_admin(question, user))

    sections.append(navsection_question_common(question, user))

    return navbar(sections)
