"""
The "points" track
==================

The points track advance as user accumulates points.
"""

from django.utils.translation import ugettext_lazy as _

from .base import BadgeTrack, Badge


class PointsBadge(Badge):
    """
    Each badge is determined by a certain amount of owned points.
    """
    class Meta:
        proxy = True


class PointsBadgeTrack(BadgeTrack):
    """
    You achieve medals in the points track by accumulating points in the
    Codeschool system.
    """

    class Meta:
        proxy = True

    badge_class = PointsBadge

    #
    # Namespace of badge constructors in the track
    #
    @classmethod
    def badge(cls, points: int, slug, title, description, message=None,
              **kwargs):
        if message is None:
            message = _('Achieve %(points) points.') % {'points': points}
        kwargs['points'] = points
        return cls.badge(slug, title, message, description, **kwargs)

    @classmethod
    def padawan_badge(cls):
        return cls.badge(
            10, 'padawan',
            _('Starter'),
            _('Congratulations padawan! You are just starting in Codeschool. '
              'Keep it going to receive prizes and glory :)'),
            message=_('First level badge.'),
        )

    @classmethod
    def junior_badge(cls):
        return cls.badge(
            100, 'junior',
            _('Junior'),
            _('100 points! Wow!'),
        )

    @classmethod
    def aprentice_badge(cls):
        return cls.badge(
            500, 'aprentice',
            _('Aprentice'),
            _('I can see you are improving your skills...'),
        )

    @classmethod
    def rookie_badge(cls):
        return cls.badge(
            1000, 'rookie',
            _('Rookie'),
            _('I see you have a bright future ahead.'),
        )

    @classmethod
    def junior_programmer_badge(cls):
        return cls.badge(
            2000, 'junior-programmer',
            _('Junior programmer'),
            _('I see you enjoy programming, huh?'),
        )

    @classmethod
    def programmer_badge(cls):
        return cls.badge(
            5000, 'programmer',
            _('Programmer'),
            _('Tell me your Github! I see you are a programmer now.'),

        )

    @classmethod
    def skilled_programmer_badge(cls):
        return cls.badge(
            10000, 'skilled-programmer',
            _('Skilled programmer'),
            _('Your code rises above the crowd...'),
        )

    @classmethod
    def programming_master_badge(cls):
        return cls.badge(
            10000, 'programming-master',
            _('Programming Master'),
            _('Code is your weapon.'),
        )

    @classmethod
    def hacker_badge(cls):
        return cls.badge(
            50000, 'hacker',
            _('Hacker'),
            _('You\'ve implemented the code in which legends are written.'),
        )