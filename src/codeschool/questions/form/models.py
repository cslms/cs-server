from datetime import date

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from lazyutils import lazy

from codeschool import models
from codeschool.questions.base.models import Question


class FormQuestion(Question):
    """
    FormQuestion's defines a question with multiple fields that can be
    naturally represented in a web form. A FormQuestion thus expect a response
    """


class FormEntry(models.Model):
    """
    An entry in a form.
    """

    TYPE_STRING, TYPE_TEXT, TYPE_BOOLEAN, TYPE_INT, TYPE_FLOAT, TYPE_DATE = \
        range(5)

    TYPE_CHOICES = [
        (TYPE_STRING, _('String')),
        (TYPE_TEXT, _('Text')),
        (TYPE_BOOLEAN, _('Boolean')),
        (TYPE_INT, _('Integer')),
        (TYPE_FLOAT, _('Numeric')),
        (TYPE_DATE, _('Date')),
    ]
    TYPE_MAP = {
        TYPE_STRING: str,
        TYPE_TEXT: str,
        TYPE_BOOLEAN: bool,
        TYPE_INT: int,
        TYPE_FLOAT: float,
        TYPE_DATE: date,
    }

    form = models.ForeignKey(
        FormQuestion,
        related_name='entries',
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=30)
    label = models.CharField(max_length=40)
    help = models.CharField(max_length=140, help_text=True)
    type = models.SmallIntegerField(choices=TYPE_CHOICES)
    default = models.CharField(max_length=40, blank=True)
    placeholder = models.CharField(max_length=40, blank=True)
    grader_json = models.JSONField()

    class Meta:
        unique_together = [('name', 'form')]

    @property
    def py_type(self):
        return self.TYPE_MAP[self.type]

    @lazy
    def grader(self):
        return answer_from_json(self.grader_json)

    def clean(self):
        if self.default and not self._can_have_default():
            raise ValidationError({
                'default': _(
                    'cannot define default values for this type of field.'
                )
            })
        self._validate_default()

        if self.placeholder and not self._can_have_placeholder():
            raise ValidationError({
                'placeholder': _(
                    'cannot define a placeholder for this type of field.'
                )
            })

    def _can_placeholder(self):
        return self.py_type != bool

    def _can_have_default(self):
        return self.py_type in {str, int, float, date}

    def _validate_default(self):
        tt = self.py_type
        data = self.default

        try:
            if tt in {int, float}:
                tt(data)
            elif tt == date:
                yy, dd, aa = map(int, date.split('/'))
            elif tt == bool:
                if data not in {'true', 'false'}:
                    raise ValueError
        except (ValueError, IndexError) as ex:
            raise ValidationError({'default': 'invalid default value'})
        return self


def answer_from_json(json):
    """
    Return an Grader sub-instance from the given JSON data.
    """
