from collections import Counter

from codeschool import models


class GivenPointsQuerySet(models.QuerySet):
    """
    Queryset for GivenPoints models.
    """

    def issue_points(self, user, value, token, index=None):
        """
        Issue points for the given token.

        The points must be associated with a token string and (optionally) to
        an index.  If the token object is a Django model instance, it is
        interpreted as the object's "app_label.Model" and the index becomes
        the object's pk.
        """

        # Fetch token from object.
        if isinstance(token, models.Model):
            index = token.pk
            label = token._meta.app_label
            class_name = token.__class__.__name__
            token = "@%s.%s" % (label, class_name)

        handler = self.get_or_create(user=user, token=token, index=index)
        if handler.points != value:
            handler.points = value
            handler.save(update_fields=['points'])

    def total_score(self, user):
        """
        The total Xp points associated to the given user.
        """

        points = self.filter(user=user).values_list('points', flat=True)
        return sum(points)

    def leaderboard(self, token, index=None):
        """
        Construct the leaderboard from all GivenPoints entries for the given
        token.

        Leaderboard is a values queryset of (user, points) pairs sorted
        from higher to lower.
        """

        self._leaderboard_cache = counter = Counter()
        values = self \
            .select_related('user') \
            .values_list('user', 'points')

        for user, points in values:
            counter[user] += points
        return counter


class ScoreQuerySet(models.QuerySet):
    """
    Table level logic for GlobalAchievement.
    """

    def leaderboard(self):
        """
        Return the global leaderboard.

        Leaderboard is a values queryset of (user, points) pairs sorted
        from higher to lower.
        """

        return self.order_by('-points').values_list('user', 'points')

    def ranking(self, user):
        """
        Return the 0-based user's ranking in the leaderboard.
        """

        points = self.get_or_create(user=user, points=0).points
        return self.filter(points__gt=points).count()
