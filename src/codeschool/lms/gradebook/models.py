from django.utils.translation import ugettext_lazy as _
from codeschool import models


class Gradebook(models.CodeschoolPage):
    """
    The gradebook page for each student.

    Each student have a gradebook object for each of its enrolled courses.
    """

    user = models.ForeignKey(
        'auth.User',
        verbose_name=_('Student name'),
        on_delete=models.PROTECT,
    )
    course = models.ForeignKey(
        'cs_core.Course',
        on_delete=models.SET_NULL,
        null=True,
    )

    # Wagtail admin
    parent_page_types = ['cs_core.Profile']