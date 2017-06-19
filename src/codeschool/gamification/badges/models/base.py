from django.utils.translation import ugettext_lazy as _

from codeschool import models


class BadgeTrack(models.PolymorphicModel):
    """
    A badge track represents a single type of action that can give several
    badges for different levels of accomplishment.
    """

    name = models.CharField(
        _('name'),
        max_length=200,
    )
    slug = models.SlugField(
        unique=True
    )
    description = models.TextField(
        _('description'),
        help_text=_(
            'A detailed description of the badge track.'
        ),
    )
    extra = models.JSONField(default=dict)
    badge_class = None

    @classmethod
    def instance(cls):
        """
        Returns the default instance for the given track.
        """

        return cls()

    @classmethod
    def badge(cls, slug, name, description, message, **kwargs):
        """
        Construct a badge instance in the current track.
        """

        return cls.badge_class(
            track=cls.instance(),
            name=name,
            slug=slug,
            description=description,
            message=message,
            **kwargs
        )


class Badge(models.TimeStampedModel, models.PolymorphicModel):
    """
    An abstract badge that marks an accomplishment in a given badge track.
    """

    track = models.ForeignKey(
        BadgeTrack,
        related_name='badges'
    )
    name = models.CharField(
        _('name'),
        max_length=200,
    )
    slug = models.CharField(
        unique=True
    )
    description = models.TextField(
        _('description'),
        help_text=_(
            'A detailed description of the accomplishment required to receive '
            'the badge.'
        ),
    )
    message = models.TextField(
        _('message'),
        help_text=_(
            'The message displayed when users receive the given badge'
        )
    )
    image = models.ImageField(
        upload_to='gamification/badges/',
        blank=True,
        null=True,
    )
    required_achievement = models.PositiveIntegerField(
        default=0,
        help_text=_(
            'Abstract quantity that associated with linear badge tracks.'
        ),
    )
    level = models.PositiveIntegerField(
        _('Badge level'),
        help_text=_(
            'The badge level: for linear badge tracks, it defines the ordering'
            'between different badges.'
        ),
    )
    extra = models.JSONField(
        default=dict,
    )
    users = models.ManyToManyField(
        models.User,
        through='GivenBadge',
        related_name='badges',
    )

    def issue_badge(self, user):
        """
        Issue badge for the given user.
        """

        self.users.add(user)


class GivenBadge(models.TimeStampedModel):
    """
    Implements a M2M relationship between badges and users.
    """

    user = models.ForeignKey(models.User, related_name='+')
    badge = models.ForeignKey(Badge, related_name='+')
