from codeschool import models
from .managers import GivenPointsQuerySet, ScoreQuerySet


class GivenPoints(models.TimeStampedModel):
    """
    Handles users experience points for any given event.

    Points are associated to a unique (user, token, index) tuple. The token +
    index pair is used to identify resources in codeschool that may emmit
    points. This resources can be model instances or any arbitrary combination
    of string and ints.
    """

    user = models.ForeignKey(models.User)
    points = models.IntegerField(default=0)
    token = models.CharField(max_length=100)
    index = models.IntegerField(blank=True, null=True)

    objects = GivenPointsQuerySet.as_manager()

    class Meta:
        unique_together = [('user', 'token', 'index')]


class Score(models.Model):
    """
    A cache to keep track of the total number of points issued to each user.

    This can be recreated at any type from the GivenPoints table.
    """

    user = models.OneToOneField(
        models.User,
        primary_key=True,
        related_name='score',
    )
    points = models.PositiveIntegerField()

    objects = ScoreQuerySet.as_manager()

    class Meta:
        ordering = '-points', 'user'

    def __int__(self):
        return self.points
