#
# This is currenlty not used. It will be better to refactor it to a separate
# class that interacts with Feedback instances and store info on points, xp and
# stars.
#


class FeedbackPatch:
    """
    Gamify lms.activities.Feedback
    """

    points_total = property(lambda x: x.submission.points_total)
    stars_total = property(lambda x: x.submission.stars_total)

    def final_points(self):
        """
        Return the amount of points awarded to the submission after
        considering all penalties and bonuses.
        """

        return self.final_grade_pc * self.points_total / 100

    def given_points(self):
        """
        Compute the number of points that should be awarded to the submission
        without taking into account bonuses and penalties.
        """

        return self.given_grade_pc * self.points_total / 100

    def final_stars(self):
        """
        Return the amount of stars awarded to the submission after
        considering all penalties and bonuses.
        """

        return self.final_grade_pc * self.stars_total / 100

    def given_stars(self):
        """
        Compute the number of stars that should be awarded to the submission
        without taking into account bonuses and penalties.
        """

        return self.given_grade_pc * self.stars_total / 100


class SubmissionPatch:
    points_total = property(lambda x: x.progress.activity.points_total)
    stars_total = property(lambda x: x.progress.activity.stars_total)

    def update_response_score(self, commit=True):
        """
        Recompute points and starts for submission and update the corresponding
        response structure.
        """

        updated = False
        response = self.progress
        score = response.points, response.stars, response.score

        if self.points < self.given_points():
            self.points = self.given_points()
            self.save(update_fields=['points'])
        if self.stars < self.given_stars():
            self.stars = self.given_stars()
            self.save(update_fields=['stars'])

        if response.points < self.points:
            updated = True
            response.points = self.points

        if response.stars < self.stars:
            updated = True
            response.stars = self.stars

        if response.score < self.score:
            updated = True
            response.score = self.score

        if updated:
            new = response.points, response.stars, response.score
            logger.info('(%s) score: %s -> %s' % (self, score, new))

        if commit and updated:
            response.save()
        return updated
