from collections import Counter
from time import time

from decimal import Decimal
from django.utils.translation import ugettext_lazy as _
from lazyutils import lazy, lazy_classattribute

from codeschool import models


class GivenXpQuerySet(models.QuerySet):
    pass


class _GivenXpManager(models.Manager):

    def update(self, user, value, token, index=None):
        """
        Set user experience points to "points".

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
            token = "%s.%s" % (label, class_name)

        handler = self.get_or_create(user=user, token=token, index=index)
        if handler.points != value:
            handler.points = value
            handler.save(update_fields=['points'])

GivenXpManager = _GivenXpManager.from_queryset(GivenXpQuerySet)


class GivenXp(models.Model):
    """
    Handles users experience points.
    """

    class Meta:
        unique_together = [('user', 'token', 'index')]

    user = models.ForeignKey(models.User)
    points = models.IntegerField(default=0)
    token = models.CharField(max_length=100)
    index = models.IntegerField(blank=True, null=True)
    objects = GivenXpManager()
    _leaderboard_expire_time = time() - 1  # begin at expired state

    @classmethod
    def total_score(cls, user):
        """
        The total Xp points associated to the given user.
        """

        points = cls.objects.filter(user=user).values_list('points', flat=True)
        return sum(points)

    @classmethod
    def leaderboard(cls, force_refresh=False):
        """
        Construct the leaderboard from all GivenXp entries.

        The leaderboard is cached and refreshed at most every 5min.
        """

        if force_refresh or time() <= cls._leaderboard_expire_time:
            cls._leaderboard_cache = counter = Counter()
            values = cls.objects\
                .select_related('user')\
                .values_list('user', 'points')

            for user, points in values:
                counter[user] += points
            cls._leaderboard_expire_time = time() + 5 * 60

        return cls._leaderboard_cache


class GlobalAchievement(models.Model):
    user = models.ForeignKey(models.User)
    score = models.FloatField()
    token = models.CharField(max_length=100)


class ScoreHandler(models.TimeStampedModel):
    """
    Common implementations for TotalScores and UserScores.
    """

    class Meta:
        abstract = True

    page = models.ForeignKey(models.Page, related_name='+')
    points = models.IntegerField(default=0)
    stars = models.DecimalField(default=Decimal(
        0), decimal_places=1, max_digits=5)

    @lazy_classattribute
    def _wagtail_root(cls):
        return models.Page.objects.get(path='0001')

    @lazy
    def specific(self):
        return self.page.specific

    def get_parent(self):
        """
        Return parent resource handler.
        """

        raise NotImplementedError('must be implemented in subclasses')

    def get_children(self):
        """
        Return a queryset with all children resource handlers.
        """

        raise NotImplementedError('must be implemented in subclasses')

    def set_diff(self, points=0, stars=0, propagate=True, commit=True,
                 optimistic=False):
        """
        Change the given resources by the given amounts and propagate to all
        the parents.
        """

        # Update fields
        kwargs = {}
        if points and (points > 0 or not optimistic):
            self.points += points
            kwargs['points'] = points
        if stars and (stars > 0 or not optimistic):
            self.stars += stars
            kwargs['stars'] = stars

        if kwargs and commit:
            self.save(update_fields=kwargs.keys())

        # Propagate to all parent resources
        if propagate and kwargs and commit:
            parent = self.get_parent()
            kwargs['commit'] = True
            kwargs['propagate'] = True
            if parent is not None:
                parent.set_diff(optimistic=False, **kwargs)

    def set_values(self, points=0, stars=0, propagate=True, optimistic=False,
                   commit=True):
        """
        Register a new value for the resource.

        If new value is greater than the current value, update the resource
        and propagate.

        Args:
            points, score, stars, (number):
                New value assigned to each specified resource.
            propagate (bool):
                If True (default), increment all parent nodes.
            optimistic (bool):
                If True, only update if give value is greater than the
                registered value.
            commit (bool):
                If True (default), commit results to the database.
        """

        d_points = points - self.points
        d_stars = Decimal(stars) - self.stars

        self.set_diff(points=d_points, stars=d_stars, propagate=propagate,
                      commit=commit, optimistic=optimistic)


class TotalScore(ScoreHandler):
    """
    Stores the maximum amount of resources that can be associated with each
    page.

    Resources can be score, points, or stars.
    """

    class Meta:
        unique_together = [('page',)]

    @lazy
    def total_attribute_name(self):
        return self.resource_name + '_value'

    @lazy
    def resource_name(self):
        return self.__class__.__name__.lower()[:-5]

    @classmethod
    def load(cls, page):
        """
        Return TotalScore object for the given page.
        """

        score, created = cls.objects.get_or_create(page=page)
        return score

    @classmethod
    def update(cls, page, **kwargs):
        """
        Updates the total resources of the given user/page pair.

        Accept the same keyword arguments as the .set_values() method.
        """

        score = cls.load(page)
        score.set_values(**kwargs)

    def get_parent(self):
        parent_page = self.page.get_parent()
        if parent_page is None:
            return None

        return self.__class__.objects.get_or_create(page=parent_page)[0]

    def get_children(self):
        children_pages = self.page.get_children()
        return [self.load(page) for page in children_pages]

    def contribution(self):
        """
        Return the contribution of the current page to the resource total.
        """

        data = Counter()
        if hasattr(self.specific, 'get_score_contributions'):
            data.update(self.specific.get_score_contributions())
        return data

    def recompute_total(self, commit=True):
        """
        Recompute the totals for the given activity and all of its children.

        Set commit=False to prevent modifying the database.
        """

        initial = self.contribution()
        totals = [c.recompute_total(commit) for c in self.get_children()]
        result = sum(totals, initial)
        if commit:
            fields = []
            for k, v in result.items():
                fields.append(k)
                setattr(self, k, v)
            self.save(update_fields=fields)
        return result


class UserScore(ScoreHandler):
    """
    Base class for all accumulated resources.
    """

    class Meta:
        unique_together = [('user', 'page')]

    used_stars = models.DecimalField(
        default=0.0,
        decimal_places=1,
        max_digits=5
    )
    user = models.ForeignKey(models.User, related_name='+')

    @property
    def available_stars(self):
        return self.stars - self.used_stars

    @available_stars.setter
    def available_stars(self, value):
        self.used_stars = self.stars - value

    @classmethod
    def load(cls, user, page):
        """
        Return UserScore object for the given user/page.
        """
        score, created = cls.objects.get_or_create(user=user, page=page)
        return score

    @classmethod
    def update(cls, user, page, diff=False, **kwargs):
        """
        Updates the accumulated resources of the given user/page pair.

        Accept the same keyword arguments as the .set_values() method.
        """

        score = cls.load(user, page)
        if diff:
            score.set_diff(**kwargs)
        else:
            score.set_values(**kwargs)

    @classmethod
    def total_score(cls, user):
        """
        Return the total score for the given user.

        This is equivalent to the score associated with wagtail's root page.
        """

        return cls.objects.get_or_create(user=user, page=cls._wagtail_root)[0]

    @classmethod
    def leaderboard(cls, page):
        """
        Return a (points_counter, starts_counter) pair of Counter() objects
        representing a leaderboard for the given page.
        """

        stars_counter, points_counter = Counter(), Counter()
        values = cls.objects\
            .filter(page=page)\
            .select_related('user')\
            .values_list('user', 'stars', 'points')

        for user, stars, points in values:
            points_counter[user] += points
            stars_counter[user] += stars

        return points_counter, stars_counter

    def get_parent(self):
        parent_page = self.page.get_parent()
        if parent_page is None:
            return None

        return self.__class__.objects.get_or_create(user=self.user,
                                                    page=parent_page)[0]

    def get_children(self):
        children_pages = self.page.get_children()
        return [self.load(self.user, page) for page in children_pages]


class HasScorePage(models.Page):
    """
    Mixin abstract page class for Page elements that implement the Score API.

    Subclasses define points_value, stars_value, and difficulty fields that
    define how activities contribute to Codeschool score system.
    """

    class Meta:
        abstract = True

    DIFFICULTY_TRIVIAL = 0
    DIFFICULTY_VERY_EASY = 1
    DIFFICULTY_EASY = 2
    DIFFICULTY_REGULAR = 3
    DIFFICULTY_HARD = 4
    DIFFICULTY_VERY_HARD = 5
    DIFFICULTY_CHALLENGE = 6
    DIFFICULTY_CHOICES = [
        (DIFFICULTY_TRIVIAL, _('Trivial')),
        (DIFFICULTY_VERY_EASY, _('Very Easy')),
        (DIFFICULTY_EASY, _('Easy')),
        (DIFFICULTY_REGULAR, _('Regular')),
        (DIFFICULTY_HARD, _('Hard')),
        (DIFFICULTY_VERY_HARD, _('Very Hard')),
        (DIFFICULTY_CHALLENGE, _('Challenge')),
    ]
    POINTS_FROM_DIFFICULTY = {
        DIFFICULTY_TRIVIAL: 10,
        DIFFICULTY_VERY_EASY: 30,
        DIFFICULTY_EASY: 60,
        DIFFICULTY_REGULAR: 100,
        DIFFICULTY_HARD: 150,
        DIFFICULTY_VERY_HARD: 250,
        DIFFICULTY_CHALLENGE: 500,
    }
    DEFAULT_DIFFICULTY = DIFFICULTY_REGULAR

    points_total = models.IntegerField(
        _('value'),
        blank=True,
        help_text=_(
            'Points may be awarded in specific contexts (e.g., associated with '
            'a quiz or in a list of activities) and in Codeschool\'s generic '
            'ranking system.'
        )
    )
    stars_total = models.DecimalField(
        _('stars'),
        decimal_places=1,
        max_digits=5,
        blank=True,
        help_text=_(
            'Number of stars the activity is worth (fractional stars are '
            'accepted). Stars are optional bonus points for special '
            'accomplishments that can be used to trade "special powers" in '
            'codeschool.'
        ),
        default=0.0
    )
    difficulty = models.IntegerField(
        blank=True,
        choices=DIFFICULTY_CHOICES,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not kwargs:
            self._score_memo = self.points_total, self.stars_total

    def clean(self):
        if self.difficulty is None:
            self.difficulty = self.DEFAULT_DIFFICULTY

        if self.points_total is None:
            self.points_total = self.POINTS_FROM_DIFFICULTY[self.difficulty]

        super().clean()

    def save(self, *args, **kwargs):
        scores = getattr(self, '_score_memo', (0, 0))
        super().save(*args, **kwargs)

        # Update the ScoreTotals table, if necessary.
        if scores != (self.points_total, self.stars_total):
            points = self.points_total
            stars = self.stars_total
            TotalScore.update(self, points=points, stars=stars)

    def get_score_contributions(self):
        """
        Return a dictionary with the score value associated with
        points, score, and stars.
        """

        return {
            'points': self.points_total,
            'stars': self.stars_total,
        }
