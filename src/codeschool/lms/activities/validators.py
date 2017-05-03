from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


def grade_validator(grade):
    if not (0 <= grade <= 100):
        raise ValidationError(_('grade must be in the (0, 100) range!'))
