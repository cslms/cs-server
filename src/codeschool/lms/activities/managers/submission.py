from codeschool import models

DEFAULT_LEXICOGRAPHICAL_PRIORITY = (
    'given_grade', 'score', 'stars', 'final_grade'
)


class SubmissionQuerySet(models.PolymorphicQuerySet):

    def recyclable(self, submission):
        """
        Return all submissions that share the same progress object and the same
        hash.

        These are candidates for submission recycling.
        """

        hash = submission.compute_hash()
        progress = submission.progress
        return self \
            .filter(progress=progress, hash=hash) \
            .order_by('created')

    def lexicographical_priority(self, value=None):
        """
        Normalize list of priorities.
        """
        if isinstance(value, str):
            return value,
        elif value is None:
            return DEFAULT_LEXICOGRAPHICAL_PRIORITY
        else:
            return iter(value)

    def for_activity(self, activity):
        """
        Filter submissions by activity.
        """

        return self.filter(progress__activity_page=activity)

    def for_user(self, user):
        """
        Filter submissions by user.
        """

        return self.filter(progress__user=user)

    def best(self, attrs=None, activity=None):
        """
        Return the best submission in the queryset.

        Submissions are ranked lexicographically according to the result of
        .lexicographical_priority() method.

        Users may mass a different list of parameters to be compared.
        """

        attrs = self.lexicographical_priority(attrs)
        if activity is not None:
            qs = self.for_activity(activity)
        if qs.empty():
            return None

        # Filter by regular attributes: higher values are better
        for attr in attrs:
            qs = qs.order_by('-' + attr)
            best_value = getattr(qs.first(), attr)
            qs = qs.filter(**{attr: best_value})
            if qs.count() == 1:
                return qs.first()

        # Filter by creation date
        return qs.order_by('created').last()

    def best_for_user(self, user, attrs=None, activity=None):
        """
        Best submission for given user.

        Return None if no submission is found.
        """

        try:
            return self.filter(user=user).best(attrs, activity=activity)
        except models.User.DoesNotExist:
            return None

    def best_for_users(self, attrs=None, activity=None):
        """
        Return a map from users to their respective best submissions.

        Only consider submission that were graded.
        """

        best_mapping = {}
        attrs = self.lexicographical_priority(attrs)
        qs = self.order_by('created')
        if activity is not None:
            qs = qs.for_activity(activity)

        for submission in qs:
            user = submission.user
            try:
                best = best_mapping[user]
            except KeyError:
                best_mapping[user] = submission
            else:
                for attr in attrs:
                    curr_value = getattr(submission, attr)
                    best_value = getattr(best, attr)
                    if curr_value < best_value:
                        break
                else:
                    best_mapping[user] = submission

        return best_mapping

    def has_correct(self):
        """
        Return True if there is any correct answer in the queryset.
        """

        return self.filter(given_grade=100).count() >= 1


SubmissionManager = models.PolymorphicManager.from_queryset(
    SubmissionQuerySet, 'SubmissionManager'
)
