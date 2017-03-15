import model_reference

from codeschool import models


class FamilyManager:
    """
    Manages
    """

    def all(self):
        """
        Query
        """

        return self._manager.filter(original_page_id=self.original_id())

    def children(self):
        """
        Queryset over all objects that have the same "original" reference.
        """

        return self.all().exclude(id=self.original_id())

    def original(self):
        """
        Original reference.
        """

        return self._object.original

    def original_id(self):
        """
        Id from the original reference.
        """

        return self._object.original_id

    def sync_with_original(self, fields=None, exclude=None):
        """
        Update all given fields from the original reference.

        If no fields are given, all fields are updated except from those that
        define the page path and version in wagtail.
        """

    def update_children(self, fields=None, exclude=None):
        """
        Update all children from an original"
        """

    def update_all(self):
        """
        dsf
        Returns
        -------

        """
