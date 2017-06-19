from codeschool import models


class TeamABCQuerySet(models.QuerySet):
    """
    Common functionality for TeamQuerySet and PairQuerySet.
    """


class PairQuerySet(TeamABCQuerySet):
    """
    A QuerySet for pair instances.
    """

    def partition(self, users, activity=None, commit=True):
        """
        Partition users into pairs for the given activity.

        Returns a sequence of created pairs.
        """


class TeamQuerySet(TeamABCQuerySet):
    """
    A QuerySet for team instances.
    """

    def partition(self, users, activity=None, *, team_size=None,
                  n_teams=None, commit=True):
        """
        Partition users into sub-groups for the given activity.

        Args:
            users:
                A iterable over users.
            activity:
                The requested activity.
            team_size:
                If given, select the desired team size for the partition.
            n_teams:
                If given, select the number of teams. Either team_size or
                n_teams must be given.
            commit:
                Controls if groups are commited to the database.

        Returns:
            A list of groups.
        """
