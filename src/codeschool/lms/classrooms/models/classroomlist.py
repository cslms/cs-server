import model_reference
from django.utils.translation import ugettext_lazy as _

from codeschool import models


class ClassroomList(models.RoutableViewsPage,
                    models.DecoupledAdminPage):
    """
    A list of classrooms.

    This page exists with the sole purpose of being a root page for Classroom
    instances.
    """


@model_reference.factory('classroom-root')
def make_courses_list():
    """
    Creates the default site-wide courses list.

    All course pages should be children of this page.
    """

    parent_page = model_reference.load('root-page')
    courses_list = ClassroomList(
        title=_('List of classrooms'),
        slug='classes',
    )
    return parent_page.add_child(instance=courses_list)
