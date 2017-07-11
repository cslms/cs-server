from codeschool import models


class PairingsBoard(models.TimeStampedModel):
    """
    Keeps track of all pairings done in an activity.
    """

    name = models.CodeschoolNameField()
    members = models.ManyToManyField(
        models.User,
        related_name='pairing_boards',
    )


class Pairing(models.Model):
    """
    A single pairing done in a sprint.
    """

    sprint = models.ForeignKey(Sprint, related_name='pairings')
    members = models.ManyToManyField(models.User, related_name='+')
