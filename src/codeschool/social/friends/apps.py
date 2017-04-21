from django.apps import AppConfig
from django.dispatch import Signal

friendship_requested = Signal(['from_user', 'to_user', 'relation'])


class FriendsConfig(AppConfig):
    name = 'friends'
