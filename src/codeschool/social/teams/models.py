from codeschool import models
from codeschool.utils import phrases
from .managers import TeamQuerySet, PairQuerySet


class TeamABC(models.TimeStampedModel):
    """
    Common functionality between Pair and Team.
    """

    name = models.CharField(default=phrases.phrase)
    activity_ctype = models.ForeignKey(
        models.ContentType,
        blank=True,
        null=True
    )
    activity_id = models.IntegerField(
        blank=True,
        null=True
    )

    class Meta:
        abstract = True

    @property
    def activity(self):
        "Instantiated activity"
        return self.activity_ctype.get_object_for_this_type(id=self.activity_id)


class Pair(TeamABC):
    """
    A pair of students.
    """

    first_user = models.ForeignKey(models.User)
    second_user = models.ForeignKey(models.User)
    objects = PairQuerySet.as_manager()


class Team(TeamABC):
    """
    A team of many students.
    """

    students = models.ManyToManyField(models.User)
    objects = TeamQuerySet.as_manager()
