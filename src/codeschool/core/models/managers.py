from codeschool import models


class MonkeyPatcher:
    @classmethod
    def patch(cls, base):

        # Execute monkey patch
        for k, v in cls.__dict__.items():
            if k.startswith('__') or k == 'patch':
                continue

            setattr(base, k, v)


# Patch wagtail's default manager
class PageManagerPatch(MonkeyPatcher):
    """
    Monkey patchs wagtail's Page manager to add some codeschool related
    functionality.
    """

    def activities(self):
        """
        Filter-in only activity-based pages.
        """

        raise NotImplemented

    def questions(self):
        """
        Filter-in only question-based activities.
        """

        raise NotImplemented


# Patch wagtail's Page model
class PagePatch(MonkeyPatcher):
    def _user_vote(self, user, vote):
        self._add_vote('user:' + user.username, vote)

    def upvote(self, user):
        """
        Process upvote from the given user.
        """

        self._user_vote(user, +1)

    def downvote(self, user):
        """
        Process upvote from the given user.
        """

        self._user_vote(user, -1)

    def remove_vote(self, user_or_token):
        """
        Discards user's vote, if present.
        """

        if isinstance(user_or_token, str):
            self._remove_vote(user_or_token)
        else:
            self._remove_vote('user:' + user_or_token)


PageManagerPatch.patch(models.PageManager)
PagePatch.patch(models.Page)
