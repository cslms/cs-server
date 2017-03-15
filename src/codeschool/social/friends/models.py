from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from codeschool import models
from codeschool.social.friends.apps import friendship_requested


class FriendshipStatus(models.StatusModel):
    """
    Defines the friendship status between two users.
    """

    class Meta:
        unique_together = ('owner', 'other'),

    STATUS_NONE = 'none'
    STATUS_PENDING = 'pending'
    STATUS_FRIEND = 'friend'
    STATUS_UNFRIEND = 'unfriend'
    STATUS_COLLEAGUE = 'colleague'
    STATUS = models.Choices(
        (STATUS_NONE, _('none')),
        (STATUS_PENDING, _('pending')),
        (STATUS_FRIEND, _('friend')),
        (STATUS_UNFRIEND, _('unfriend')),
        (STATUS_COLLEAGUE, _('colleague'))
    )
    owner = models.ForeignKey(models.User, related_name='related_users')
    other = models.ForeignKey(models.User,
                              related_name='related_users_as_other')

    def __str__(self):
        return '%s-%s (%s)' % (self.owner, self.other, self.status)

    def clean(self):
        if self.other == self.owner:
            raise ValidationError('owner and other are the same!')

    def save(self, *args, **kwds):
        created = self.id is None
        super().save(*args, **kwds)

        if created:
            reciprocal, created = FriendshipStatus.objects.get_or_create(
                owner=self.other, other=self.owner)

            if not created:
                return

            if self.status == self.STATUS_COLLEAGUE:
                reciprocal.status = self.STATUS_COLLEAGUE
            elif self.status == self.STATUS_FRIEND:
                reciprocal.status = self.STATUS_PENDING

            reciprocal.save()

    def get_reciprocal(self):
        """
        Gets the reciprocal relationship.
        """

        return FriendshipStatus.objects.get(owner=self.other, other=self.owner)

    def request_friendship(self):
        """
        Owner asks other for friendship.

        This usually sets the reciprocal status to 'pending'. This might be
        different if other has blocked owner or if other has already asked for
        friend status.
        """

        self.status = self.STATUS_FRIEND
        self.save(update_fields=['status'])

        reciprocal = self.get_reciprocal()
        if reciprocal.status in (self.STATUS_COLLEAGUE, self.STATUS_NONE):
            reciprocal.status = self.STATUS_PENDING
            reciprocal.save(update_fields=['status'])
        # status PENDING  ==> keeps pending
        # status UNFRIEND ==> keeps unfriended
        # status FRIEND   ==> now both are friends (no change required)

        if reciprocal.status not in (self.STATUS_FRIEND, self.STATUS_UNFRIEND):
            friendship_requested.send(FriendshipStatus,
                                      from_user=self.owner,
                                      to_user=self.other,
                                      relation=self)


class Group(models.Model):
    """
    A group of students.
    """

    name = models.CharField(max_length=100)
    users = models.ManyToManyField(models.User, related_name='+')
