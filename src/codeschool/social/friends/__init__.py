from codeschool.utils import LazyManager
from logging import Logger

friendships = LazyManager('friends', 'friendshipstatus')
users = LazyManager('auth', 'user')
log = Logger('social.friends')


def get_all_friends(user):
    """
    Return a queryset with all user's friends.
    """

    relations = friendships.filter(owner=user, status='friend')
    user_ids = relations.values_list('other__id', flat=True)
    return users.filter(id__in=user_ids)


def get_possible_friends(user):
    """
    Return a queryset of all users that can be friend with the given user.
    """

    friends = get_all_friends(user) \
        | users.filter(id=user.id) \
        | users.filter(username='AnonymousUser')
    friends_ids = friends.values_list('id', flat=True)
    return users.exclude(id__in=friends_ids)


def request_friendship(user, other):
    """
    Mark 'other' as a friend of 'user'.

    This will create a 'pending' reverse relationship.
    """

    relation, created = friendships.get_or_create(owner=user, other=other)
    relation.request_friendship()
    log.info('friendship request: %s/%s' % (user, other))
