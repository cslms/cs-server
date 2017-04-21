class Stats:
    def get_statistics(self, user, **kwargs):
        """
        Return a dictionary with relevant statistics for activity.
        """

        return {
            'user_submissions': self.submissions.for_user(user).count(),
            'total_submissions': self.submissions.count(),
        }

    def best_submissions(self, context):
        """
        Return a dictionary mapping users to their best responses.
        """

        mapping = {}
        responses = self.responses.filter(context=context)
        for response in responses:
            mapping[response.user] = response.best_submission()
        return mapping
