"""
The "polyglot" track
====================

For accomplishments related to users submitting responses in different
programming languages or different exercice styles.
"""

from django.utils.translation import ugettext_lazy as _

from .base import BadgeTrack, Badge


class PolyglotBadge(Badge):
    class Meta:
        proxy = True


class PolyglotBadgeTrack(BadgeTrack):
    """
    You achieve medals in the polyglot track by submitting correct solutions
    to problems in different programming languages.
    """

    class Meta:
        proxy = True

    badge_class = PolyglotBadge

    #
    # Namespace of badge constructors in the track
    #
    @classmethod
    def bilingual_badge(cls):
        return cls.badge(
            'bilingual',
            _('Bilingual'),
            _('For correct submissions in two different languages.'),
            _('Congratulations! You showed you can code in two different '
              'languages.'),
        )

    @classmethod
    def polyglot_badge(cls):
        return cls.badge(
            'polyglot',
            _('Polyglot'),
            _('For correct submissions in 4 different languages.'),
            _('You are very versatile! You just submited code in four '
              'different programming languages.'),
        )
