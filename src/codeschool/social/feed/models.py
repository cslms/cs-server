from collections import OrderedDict
from django.utils.translation import ugettext_lazy as _
from codeschool import models


class Post(models.TimeStampedModel, models.PolymorphicModel):
    """
    Represents a post in the user time-line.
    """

    VISIBILITY_PUBLIC = 1
    VISIBILITY_FRIENDS = 0
    VISIBILITY_OPTIONS = [
        (VISIBILITY_FRIENDS, _('Friends only')),
        (VISIBILITY_PUBLIC, _('Pubic')),
    ]

    user = models.ForeignKey(models.User)
    text = models.RichTextField()
    visibility = models.IntegerField(
        choices=VISIBILITY_OPTIONS, default=VISIBILITY_FRIENDS)

    def __str__(self):
        return 'Post by %s at %s' % (self.user, self.created)


class CodePost(Post):
    """
    Post some code.
    """

    language = models.ForeignKey('core.ProgrammingLanguage', related_name='+')
    source = models.TextField()


def list_post_types():
    """
    Return an ordered map with post types names to their respective models.
    """
    return OrderedDict([
        ('Simple', Post),
        ('Code', CodePost),
    ])
