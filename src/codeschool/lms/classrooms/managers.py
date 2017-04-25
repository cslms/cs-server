from codeschool import models


class ClassroomQuerySet(models.PageQuerySet):

    def enrolled(self, user):
        """
        Return a list of all courses in which the user is either as a student,
        a teacher or staff member.
        """

        return (user.classrooms_as_teacher.all()
                | user.classrooms_as_student.all()
                | user.classrooms_as_staff.all())

    def open_for_user(self, user):
        """
        List of courses that the user can subscribe.
        """

        user_courses = self.for_user(user)
        qs = self.filter(is_public=True, accept_subscriptions=True,
                         live=True)
        return qs.exclude(id__in=user_courses)


# Fix bug on Wagtail
ClassroomManager = models.PageManager.from_queryset(ClassroomQuerySet)
ClassroomManager.get_queryset = models.Manager.get_queryset