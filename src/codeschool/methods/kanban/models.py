from django.utils.translation import ugettext_lazy as _

from codeschool import models


# Check for UI ideas at https://leankit.com/learn/kanban/kanban-board/
class Kanban(models.TimeStampedModel):
    """
    Represents a Kanban board activity.
    """

    name = models.CodeschoolNameField()
    members = models.ManyToManyField(
        models.User,
        related_name='kanban_boards',
    )


class TaskQuerySet(models.QuerySet):
    def todo(self):
        """
        Filter "to-do" tasks.
        """
        return self.filter(status=Task.STATUS_TODO)

    def doing(self):
        """
        Filter "doing" tasks.
        """
        return self.filter(status=Task.STATUS_DOING)

    def done(self):
        """
        Filter "done" tasks.
        """
        return self.filter(status=Task.STATUS_DONE)


class Task(models.TimeStampedModel):
    """
    Represents a task in a Kanban activity.
    """

    STATUS_TODO, STATUS_DOING, STATUS_DONE = range(3)
    STATUS_CHOICES = [
        (STATUS_TODO, _('To do')),
        (STATUS_DOING, _('Doing')),
        (STATUS_DONE, _('Done')),
    ]

    name = models.CodeschoolNameField()
    description = models.CodeschoolDescriptionField()
    status = models.SmallIntegerField(
        _('status'),
        choices=STATUS_CHOICES,
    )
    members = models.ManyToManyField(
        models.User,
        related_name='kanban_tasks',
    )
    created_by = models.ForeignKey(
        models.User,
        related_name='created_tasks',
        null=True,
        blank=True,
    )
    assigned_to = models.ManyToManyField(
        models.User,
        related_name='assigned_tasks',
    )
    estimated_duration_hours = models.PositiveSmallIntegerField(
        _('Estimated duration (hours)'),
        default=0,
    )

    objects = TaskQuerySet.as_manager()
