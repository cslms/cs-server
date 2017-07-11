from typing import Optional


class Grader:
    """
    A answer object.
    """

    def grade(self, value):
        raise NotImplementedError


class NumericGrader(Grader):
    """
    Numeric float values.
    """

    fields = {
        'max': Optional(float),
        'min': Optional(float),
        'answer': float,
        'tolerance': 0.0
    }

    def grade(self, value):
        tol = self.tolerance
        return 100 if abs(value - self.answer) <= tol else 0


class IntegerGrader(Grader):
    """
    Numeric grader for integer values
    """

    fields = {
        'max': Optional(int),
        'min': Optional(int),
        'answer': int,
    }

    def grade(self, value):
        return 100 if self.answer == value else 0

