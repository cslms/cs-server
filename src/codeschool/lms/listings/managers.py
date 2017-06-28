import model_reference
from django.db import transaction
from django.utils.translation import ugettext as _
from wagtail.wagtailcore.models import PageManager

from codeschool import models


class ActivitySectionQuerySet(models.PageQuerySet):

    def create_from_parent(self, parent=None, **kwargs):
        """
        Create a new ActivityList using the given keyword arguments under the
        given parent page. If no parent is chosen, uses the main Wagtail root
        page.
        """

        kwargs.update(
            title=_('Activities'),
            short_description=kwargs.get('short_description',
                                         _('List of activities.')),
            slug='activities',
        )
        parent = parent or model_reference.load('root-page')
        new = self.model(**kwargs)
        parent.add_child(instance=new)
        new.save()
        return new

    def create_from_template(self, template, parent=None):
        """
        Creates a new instance from the given template.

        Valid templates are:
            programming-beginner
                Basic sections in a beginner programming course.
            programming-intermediate
                Sections for a second course on programming course.
            programming-marathon
                Sections for a marathon based course.
        """

        with transaction.atomic():
            new = self.create_from_parent(parent)
            new.update_from_template(template)
            return new

    def main(self):
        """
        Return the main ActivityList for the website.
        """

        return model_reference.load('root-page', model=self.model)


ActivitySectionManager = PageManager.from_queryset(ActivitySectionQuerySet)
