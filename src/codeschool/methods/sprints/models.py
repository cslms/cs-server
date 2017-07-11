from django.utils.translation import ugettext_lazy as _

from codeschool import models


class Sprint(models.TimeStampedModel):
    """
    A sprint meta-data object that can be associated with many
    projects/contexts.
    """

    index = models.PositiveSmallIntegerField()
    start_date = models.DateField(
        _('Starts'),
    )
    due_date = models.DateField(
        _('Ends'),
    )
    name = models.CodeschoolNameField(blank=True)
    description = models.CodeschoolDescriptionField(blank=True)

    def next_sprint(self, name='', description=''):
        """
        Schedule a new sprint starting at the end of the current sprint and
        keeping the same time-frame.
        """

        raise NotImplementedError
