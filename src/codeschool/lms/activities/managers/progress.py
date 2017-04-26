import csv
import io

from codeschool import models


class ProgressQuerySet(models.PolymorphicQuerySet):

    def _get_activity(self, activity):
        # Fetch activity from related manager. This makes it usable from a
        # queryset related to an activity without having to explicitly pass the
        # activity instance
        if activity is None:
            try:
                return self._hints['instance']
            except (KeyError, AttributeError):
                msg = "missing required positional argument 'activity'"
                raise TypeError(msg)
        return activity

    def correct(self):
        """
        Filter only correct responses.
        """

        return self.filter(is_correct=True) | self.filter(grade=100)

    def for_request(self, request, activity=None):
        """
        Return progress instance associated with the request object.

        This usually means using the .user attribute from the request.
        """

        return self.for_user(request.user, activity)

    def for_user(self, user, activity=None):
        """
        Return progress associated with the given user and activity page.
        """

        activity = self._get_activity(activity)
        response, _ = self.get_or_create(user=user, activity_page=activity)
        return response

    def gradebook(self, activity=None, *,
                  fields=('final_grade_pc',),
                  user_fields=('username',), order_by=None):
        """
        Return a table collecting all progress data from a given activity.

        Args:
            activity:
                The activity page.
            fields:
                List of field names extracted from each Progress object. By
                default it only selects the 'final_grade_pc' field.
            user_fields:
                List of fields to be extracted from the user object. By default
                it only selects 'username'.
            order_by:
                Field used for sorting results. It uses the first selected user
                field by default.

        Returns:
            A list of tuples of the form::

                [
                    (username_0, final_grade_pc_0),
                    (username_1, final_grade_pc_1),
                    ...
                ]
        """
        if not user_fields:
            raise ValueError('must provide at least one user field.')
        if order_by is None:
            order_by = 'user__' + user_fields[0]

        fields = ['user__' + f for f in user_fields] + list(fields)
        activity = self._get_activity(activity)
        return list(
            self.filter(activity_page=activity)
                .order_by(order_by)
                .values_list(*fields)
        )

    def gradebook_csv(self, activity=None, *,
                      header=True, dialect='excel',
                      fields=('final_grade_pc',), user_fields=('username',),
                      order_by=None):
        """
        Similar to the gradebook function, but return a CSV string.

        This accepts all arguments of :meth:`gradebook`, plus the following.

        Args:
            header:
                If True (default), prints a header.


        Returns:
            A string of CSV data.
        """

        rows = self.gradebook(activity,
                              fields=fields,
                              user_fields=user_fields,
                              order_by=order_by)

        # Write CSV data on a StringIO file and fetch its value
        F = io.StringIO()
        writer = csv.writer(F, dialect=dialect)

        if header:
            writer.writerow(tuple(user_fields) + tuple(fields))
        writer.writerows(rows)
        return F.getvalue()

    def users(self, activity=None):
        """
        Return a queryset with all users that made a submission to the given
        activity.
        """

        activity = self._get_activity(activity)
        qs = self.filter(activity=activity)
        user_ids = qs.values_list('user', flat=True)
        return models.User.objects.in_bulk(user_ids)


ProgressManager = \
    models.PolymorphicManager.from_queryset(
        ProgressQuerySet, 'ProgressManager')
