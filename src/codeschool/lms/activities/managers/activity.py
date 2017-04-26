from codeschool import models


class ActivityQueryset(models.PageQuerySet):

    def auth(self, user, role=None):
        """
        Filter only activities that the user can see.
        """

        return self.filter(live=True)

    def from_file(self, path, parent=None):
        """
        Creates a new object from file path.
        """

        return self.model.load_from_file(path, parent)


ActivityManager = models.PageManager.from_queryset(ActivityQueryset)
