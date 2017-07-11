import decimal
import json
from django.utils.translation import ugettext_lazy as _
from wagtail.wagtailsnippets.models import register_snippet
from wagtail.wagtailadmin import edit_handlers as panel
from codeschool import models
ZERO = decimal.Decimal(0)


def mk_grading_constructor(name):
    """
    Factory function for creating grading method constructors.
    """

    @classmethod
    def new(cls):
        try:
            return cls.objects.get(name=name)
        except cls.DoesNotExist:
            return cls.objects.create(name=name)

    new.__name__ = name
    new.__docs__ = """Return the %r grading method.""" % name
    return new


@register_snippet
class GradingMethod(models.Model):
    """
    Describes a valid grading method.
    """

    class Meta:
        unique_together = [('name', 'owner')]

    VALID_NAMES = {
        'best': _('The final grade is equal to the best response.'),
        'worst': _('The final grade is equal to the worst response.'),
        'first': _('Only the first response is considered.'),
        'last': _('Only the last response is considered.'),
        'average': _('Take the average over all responses.'),
    }
    VALID_FAMILIES = []

    name = models.CharField(
        max_length=20
    )
    description = models.TextField(
        blank=True
    )
    family = models.CharField(
        max_length=20,
        blank=True
    )
    data = models.TextField()
    owner = models.ForeignKey(
        models.User,
        blank=True,
        null=True,
        related_name='private_grading_methods',
    )
    data_as_json = property(lambda x: json.loads(x.data))

    def __str__(self):
        return self.name

    # Alternative constructors
    best = mk_grading_constructor('best')
    worst = mk_grading_constructor('worst')
    first = mk_grading_constructor('first')
    last = mk_grading_constructor('last')
    average = mk_grading_constructor('average')

    @classmethod
    def from_name(cls, name, user=None):
        """
        Return the grading method with the given name for the given user.
        """

        if name in self.VALID_NAMES:
            return getattr(self, name)()
        elif user:
            return cls.objects.get(name=name, user=user)
        else:
            raise cls.DoesNotExist

    def save(self, *args, **kwargs):
        self.validate()
        super().save(*args, **kwargs)

    def is_valid(self):
        """
        Return true if name, family and data fields are valid.
        """

        if self.name in self.VALID_NAMES:
            return self.family == '' and self.data == ''
        elif self.name == '':
            if self.family:
                try:
                    self.parse_data()
                    return True
                except ValueError:
                    return False
            else:
                return False
        else:
            return False

    def validate(self):
        """
        Validate the name, family and data fields.
        """

        if not self.is_valid():
            raise ValueError('invalid grading method')

    def parse_data(self):
        """
        Return an usable representation of data for the given family of grading
        methods.
        """

        if self.name or not self.family:
            raise ValueError
        else:
            try:
                method = getattr(self, '_parse_data_' + self.family_attribute)
            except AttributeError:
                raise ValueError
            else:
                return method()

    # Implements grading methods
    def grade(self, responses):
        """
        Grade the given sequence of responses using the grading method.
        """
        responses = list(self._filter_valid_responses(responses))
        name = self.name

        if name in ['best', 'worst']:
            func = max if name == 'best' else min
            if responses:
                return func(x.final_grade for x in responses)
            else:
                return ZERO
        elif name in ['first', 'last']:
            if responses:
                responses = sorted(responses, key=response.created)
                return response[0 if name == 'first' else -1]
            return ZERO
        elif name == 'average':
            if responses:
                return sum(x.final_grade for x in responses) / len(responses)
            else:
                return ZERO

        if self.name in self.VALID_NAMES:
            method = getattr(self, '_grade_' + self.name)
            return method(responses)
        else:
            raise NotImplementedError

    def _filter_valid_responses(self, responses):
        for response in responses:
            if response.status == response.STATUS_PENDING:
                response.autograde_response()
            if response.status == response.STATUS_DONE:
                yield response

    # Wagtail admin
    panels = [
        panel.FieldPanel('name'),
        panel.FieldPanel('description'),
    ]
