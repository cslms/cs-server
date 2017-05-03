import model_reference
from wagtail.wagtailcore.models import PageManager

from codeschool import models


class ActivitySectionQuerySet(models.PageQuerySet):
    def create_subpage(self, parent, **kwargs):
        """
        Return a new page as a child of the given parent page.
        """

        return self.model.create_subpage(parent, **kwargs)

    def main(self):
        """
        Return the main ActivityList for the website.
        """

        return model_reference.load('root-page', model=self.model)


ActivitySectionManager = PageManager.from_queryset(ActivitySectionQuerySet)
