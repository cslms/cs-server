from lazyutils import delegate_to


class CommitMixin:
    """
    Methods that saves object or not depending on the value of the commit
    variable.

    Commit can be disabled globally (eg., for tests) if the DISABLE_COMMIT
    attribute is set to True.
    """

    LAST_COMMIT_ID = 0
    DISABLE_COMMIT = False

    def commit(self, commit, *args, **kwargs):
        """
        Saves object if commit=True and return itself.
        """

        if self.DISABLE_COMMIT and commit:
            CommitMixin.LAST_COMMIT_ID += 1
            self.id = CommitMixin.LAST_COMMIT_ID
        elif commit:
            self.save(*args, **kwargs)
        return self


class FromProgressAttributesMixin:
    """
    Mixin class for submissions and feedback.

    Imports attributes from obj.progress
    """

    activity = delegate_to('progress', readonly=True)
    activity_id = delegate_to('progress', readonly=True)
    activity_title = property(lambda x: x.progress.activity_page.title)
    user = delegate_to('progress', readonly=True)
