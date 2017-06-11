import pytest
from django.core.exceptions import ValidationError

from codeschool.lms.activities.validators import grade_validator


class TestValidators:
    """
    Test generic validators
    """

    def test_grade_validador(self):
        grade_validator(0)
        grade_validator(50)
        grade_validator(100)

        with pytest.raises(ValidationError):
            grade_validator(150)
