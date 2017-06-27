from decimal import Decimal

from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from wagtail.wagtailsnippets.models import register_snippet

from codeschool import models
from codeschool import panels


@register_snippet
class Conditions(models.PolymorphicModel):
    """
    Each activity can be bound to different sets of conditions that control
    aspects on how the activity should be graded and may place restrictions on
    how the students may respond to the given activity.
    """

    class Meta:
        verbose_name = _('conditions')
        verbose_name_plural = _('conditions')

    name = models.CharField(
        _('name'),
        max_length=140,
        blank=True,
        help_text=_(
            'A string identifier.'
        )
    )
    single_submission = models.BooleanField(
        _('single submission'),
        default=False,
        help_text=_(
            'If set, students will be allowed to send only a single '
            'submission per activity.',
        ),
    )
    delay_feedback = models.BooleanField(
        _('delay feedback'),
        default=False,
        help_text=_(
            'If set, students will be only be able to see the feedback after '
            'the activity expires its deadline.'
        )
    )
    programming_language = models.ForeignKey(
        'core.ProgrammingLanguage',
        blank=True,
        null=True,
        related_name='+',
        help_text=_(
            'Defines the required programming language for code-based student '
            'responses, when applicable. Leave it blank if you do not want to '
            'enforce any programming language.'
        )
    )
    text_format = models.ForeignKey(
        'core.FileFormat',
        blank=True,
        null=True,
        related_name='+',
        help_text=_(
            'Defines the required file format for text-based responses, when '
            'applicable. Leave it blank if you do not want to enforce any '
            'text format.'
        )
    )

    def __str__(self):
        return self.name or 'Untitled condition object.'

    panels = [
        panels.FieldPanel('name'),
        panels.MultiFieldPanel([
            panels.FieldPanel('single_submission'),
            panels.FieldPanel('delay_feedback'),
        ], heading=_('Submissions')),
        panels.MultiFieldPanel([
            panels.FieldPanel('deadline'),
            panels.FieldPanel('hard_deadline'),
            panels.FieldPanel('delay_penalty'),
        ], heading=_('Deadline')),
        panels.MultiFieldPanel([
            panels.FieldPanel('get_programming_language'),
            panels.FieldPanel('text_format'),
        ], heading=_('Deadline')),
    ]


class Deadline(models.Model):
    """
    Describes a deadline of an activity.

    Users may define soft/hard deadlines.
    """

    name = models.CharField(
        _('name'),
        max_length=140,
        blank=True,
        help_text=_(
            'A unique string identifier. Useful for creating human-friendly '
            'references to the deadline object.'
        )
    )
    start = models.DateField(
        _('start'),
        blank=True,
        null=True,
    )
    deadline = models.DateTimeField(
        _('deadline'),
        blank=True,
        null=True,
    )
    hard_deadline = models.DateTimeField(
        _('hard deadline'),
        blank=True,
        null=True,
        help_text=_(
            'If set, responses submitted after the deadline will be accepted '
            'with a penalty.'
        )
    )
    penalty = models.DecimalField(
        _('delay penalty'),
        default=25,
        decimal_places=2,
        max_digits=6,
        help_text=_(
            'Sets the percentage of the total grade that will be lost due to '
            'delayed responses.'
        ),
    )

    def get_status(self):
        """
        Return one of the strings depending on how the current time relates to
        the deadline:

        closed:
            Activity has not opened yet.
        valid:
            Current time is within the deadline.
        expired:
            Hard deadline has expired. Users cannot submit to the activity.
        penalty:
            Official deadline has expired, but users can still submit with a
            penalty.
        """

        now = timezone.now()
        if self.start is not None and now < self.start:
            return 'closed'
        elif ((self.hard_deadline is not None and now > self.hard_deadline) or
              (self.hard_deadline is None and self.deadline is not None
               and now > self.deadline)):
            return 'expired'
        elif (self.hard_deadline is not None and self.deadline < now < self.hard_deadline and
              self.deadline is not None):
            return 'penalty'
        else:
            return 'valid'

    def get_penalty(self):
        """
        Return the penalty value
        """

        status = self.get_status()

        if status == 'expired':
            return Decimal(100)
        elif status == 'penalty':
            return self.penalty
        elif status == 'valid':
            return Decimal(0)
        else:
            raise RuntimeError('cannot get penalty of closed activity')

    def revise_grade(self, grade):
        """
        Return the update grade considering any possible delay penalty.
        """

        return (100 - self.get_penalty()) * Decimal(grade) / 100


class Personalization(models.Model):
    """
    Personalize a few cosmetic aspects of the activity.
    """

    name = models.CharField(
        max_length=140
    )
    icon_src = models.CharField(
        _('activity icon'),
        max_length=50,
        blank=True,
        help_text=_(
            'Optional icon name that can be used to personalize the activity. '
            'Material icons are available by using the "material:" namespace '
            'as in "material:menu".'),
    )

    @property
    def material_icon(self):
        """
        The material icon used in conjunction with the activity.
        """

        if self.icon_src.startswith('material:'):
            return self.icon_src[9:]
        return self.default_material_icon

    @property
    def icon_html(self):
        """
        A string of HTML source that points to the icon element fo the activity.
        """

        return '<i class="material-icon">%s</i>' % self.material_icon
