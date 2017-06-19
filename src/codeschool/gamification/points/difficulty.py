from django.utils.translation import ugettext_lazy as _


class DifficultyMixin:
    """
    A mixin class that exposes a default mapping of difficulty levels and the
    DIFFICULTY_CHOICES list of tuples.
    """

    DIFFICULTY_TRIVIAL = 0
    DIFFICULTY_VERY_EASY = 1
    DIFFICULTY_EASY = 2
    DIFFICULTY_REGULAR = 3
    DIFFICULTY_HARD = 4
    DIFFICULTY_VERY_HARD = 5
    DIFFICULTY_CHALLENGE = 6
    DIFFICULTY_EPIC = 7
    DIFFICULTY_CHOICES = [
        (DIFFICULTY_TRIVIAL, _('Trivial')),
        (DIFFICULTY_VERY_EASY, _('Very Easy')),
        (DIFFICULTY_EASY, _('Easy')),
        (DIFFICULTY_REGULAR, _('Regular')),
        (DIFFICULTY_HARD, _('Hard')),
        (DIFFICULTY_VERY_HARD, _('Very Hard')),
        (DIFFICULTY_CHALLENGE, _('Challenge')),
        (DIFFICULTY_EPIC, _('Epic')),
    ]
    POINTS_FROM_DIFFICULTY = {
        DIFFICULTY_TRIVIAL: 10,
        DIFFICULTY_VERY_EASY: 30,
        DIFFICULTY_EASY: 60,
        DIFFICULTY_REGULAR: 100,
        DIFFICULTY_HARD: 150,
        DIFFICULTY_VERY_HARD: 250,
        DIFFICULTY_CHALLENGE: 500,
        DIFFICULTY_EPIC: 1000,
    }
    DEFAULT_DIFFICULTY = DIFFICULTY_REGULAR


difficulty = DifficultyMixin()