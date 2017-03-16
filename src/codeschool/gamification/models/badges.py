from lazyutils import delegate_to, lazy

from django.utils.translation import ugettext_lazy as _
from codeschool import models


class BadgeTrack(models.Model):
    """
    A badge track represents a single type of action that can give several
    badges for different levels of accomplishment.
    """

    name = models.CharField(_('name'), max_length=200)
    entry_point = models.ForeignKey(models.Page, related_name='badge_tracks')

    @lazy
    def badges_list(self):
        """
        A list of all badges in the track sorted by difficulty.
        """
        badges = list(self.badges.all())
        badges.sort(key=lambda x: x.value)
        return badges

    def issue_badges(self, user, **kwargs):
        """
        Issue all badges for the given
        """

        for badge in self.badges_list:
            badge.update_for_user(user, **kwargs)


class Badge(models.Model):
    """
    Represents an abstract badge.

    Instances of these class are not associated to specific users. GivenBadge
    makes the association between badges and users.
    """

    track = models.ForeignKey(BadgeTrack, related_name='badges')
    name = models.CharField(max_length=200)
    image = models.ImageField(
        upload_to='gamification/badges/',
        blank=True,
        null=True,
    )
    required_points = models.PositiveIntegerField(default=0)
    required_score = models.PositiveIntegerField(default=0)
    required_stars = models.PositiveIntegerField(default=0)
    description = models.TextField()
    details = models.RichTextField(blank=True)

    @property
    def value(self):
        """
        A sortable element that describes the overall badge difficulty.
        """
        return self.required_stars, self.required_points, self.required_score


class GivenBadge(models.TimeStampedModel):
    """
    Associate users with badges.
    """

    badge = models.ForeignKey(Badge)
    user = models.ForeignKey(models.User)

    # Delegate attributes
    track = delegate_to('badge')
    name = delegate_to('badge')
    image = delegate_to('badge')
    description = delegate_to('badge')
    details = delegate_to('badge')
