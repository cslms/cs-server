from django.db.models import Model, CharField
from django.utils.translation import ugettext_lazy as _
from wagtail.wagtailadmin.edit_handlers import \
    MultiFieldPanel as _MultiFieldPanel, FieldPanel as _FieldPanel
from wagtail.wagtailcore.models import Page


class ShortDescriptionPage(Page):
    """
    A mixin for a Page which has a short_description field.
    """

    class Meta:
        abstract = True

    short_description = CharField(
        _('short description'),
        max_length=140,
        help_text=_(
            'A short textual description to be used in titles, lists, etc.'
        )
    )

    def full_clean(self, *args, **kwargs):
        if self.short_description and not self.seo_title:
            self.seo_title = self.short_description
        if not self.short_description:
            self.short_description = self.seo_title or self.title
        return super().full_clean(*args, **kwargs)


class ShortDescriptionMixin(Model):
    """
    A describable page model that only adds the short_description field,
    leaving the long_description/body definition to the user.
    """

    class Meta:
        abstract = True

    short_description = CharField(
        _('short description'),
        max_length=140,
        blank=True,
        help_text=_(
            'A very brief one-phrase description used in listings.\n'
            'This field accepts mardown markup.'
        ),
    )


class AbsoluteUrlMixin:
    """
    Adds a get_absolute_url() method to a Page object.
    """

    def get_absolute_url(self, *urls):
        """
        Return the absolute url of page object.

        Additional arguments append any extra url elements as in the example::

        >>> page.get_absolute_url()
        '/artist/john-lennon'
        >>> pages.get_absolute_urls('songs', 'revolution')
        '/artist/john-lennon/songs/revolution'
        """

        # We strip the first element of the url
        base_url = '/' + self.url_path[1:].partition('/')[-1]

        if not urls:
            return base_url
        url = base_url.rstrip('/')
        return '%s/%s/' % (url, '/'.join(urls))

    def get_admin_url(self, list=False):
        """
        Return the Wagtail admin url.
        """

        if list:
            return '/admin/pages/%s/' % self.id
        return '/admin/pages/%s/edit/' % self.id

    def breadcrumb(self, include_self=False, skip=1, classnames='breadcrumb'):
        """
        Return a <ul> element with the links to all parent pages.

        Skip the given number of parent roots, the default skip number is 1.
        """

        # Get all parent pages in the parents list. We create the list
        # backwards and reverse it in the end
        pages = []
        parent = self
        if not include_self:
            parent = self.get_parent()

        while parent:
            pages.append(parent)
            parent = parent.get_parent()
        pages.reverse()

        # Skip roots
        if skip:
            pages = pages[skip:]

        # Now let us create the ul element for the breadcrumb
        lines = ['<ul class="%s">' % classnames]
        for page in pages:
            lines.append('  <li><a href="{link}">{name}</a></li>'.format(
                link=page.get_absolute_url(),
                name=page.title,
            ))
        lines.append('</ul>')
        return '\n'.join(lines)
