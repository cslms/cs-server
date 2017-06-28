import model_reference
import rules
from django.utils.translation import ugettext as _

from bricks.components.html5_tags import a
from codeschool.bricks.navigation import navsection_page_admin, navsection, navbar


def navsection_classroom_common(page, user):
    """
    Common sections for classroom pages.
    """

    links = [
        a(_('Enroll'), href='/classes/enroll/'),
    ]

    # Add new course for admin users
    if user.is_superuser:
        pk = model_reference.load('classroom-root').pk
        links.append(
            a(_('Add new classroom'), href='/admin/pages/%s/add_subpage/' % pk)
        )

    # Leave course
    if rules.test_rule('classrooms.can_leave', user, page):
        links.append(a(_('Leave classroom'), bricks_bind='leave.api'))

    return navsection(_('Classrooms'), links, href='/classes/')


def navbar_classroom(page, user):
    sections = []

    # Admin tasks
    if user.has_perm('classrooms.edit_classroom'):
        sections.append(navsection_page_admin(page, user))

    # Common section
    sections.append(navsection_classroom_common(page, user))
    return navbar(sections)


def navbar_list(page, user):
    return navbar(navsection_classroom_common(page, user))
