#
# One stop shop for models, fields and managers
#
from django.db.models.fields.related_descriptors import \
    ReverseManyToOneDescriptor
from lazyutils import lazy

from .fields import *

from django.utils.translation import ugettext_lazy as _
from django.db.models import *
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User, Group, Permission

from wagtail.wagtailcore.models import Page, Orderable, PageManager, PageQuerySet
from wagtail.contrib.wagtailroutablepage.models import RoutablePage, RoutablePageMixin, route
from wagtail_model_tools.models import SinglePage, SinglePageMixin, SinglePageManager, ProxyPageMixin, CopyMixin, CopyableModel
from wagtail.wagtailadmin.edit_handlers import MultiFieldPanel as _MultiFieldPanel, FieldPanel as _FieldPanel
from modelcluster.models import ClusterableModel

from polymorphic.models import PolymorphicModel, PolymorphicManager
from polymorphic.query import PolymorphicQuerySet

from model_utils.choices import Choices
from model_utils.models import QueryManager, StatusModel, TimeFramedModel, TimeStampedModel
from model_utils.managers import QueryManager, InheritanceManager, QuerySet, InheritanceQuerySet

from codeschool.managers import *


#
# Codeschool based managers
#
class RelatedDescriptorExt(ReverseManyToOneDescriptor):
    """
    A descriptor that automatically extends the default related manager
    descriptor by inserting the given ext_class in the mro().
    """
    def __init__(self, descriptor, ext_class):
        super().__init__(descriptor.rel)
        self.descriptor = descriptor
        self.ext_class = ext_class

    @lazy
    def ext_class_final(self):
        # We test these two attributes in order to support ModelCluster
        # descriptors and the vanilla Django ones.
        for attr in ('child_object_manager_cls', 'related_manager_cls'):
            try:
                manager_cls = getattr(self.descriptor, attr)
            except AttributeError:
                continue
            else:
                class DescriptorExt(self.ext_class, manager_cls):
                    def __new__(cls, *args, **kwargs):
                        return manager_cls.__new__(cls, *args, **kwargs)

                    def __init__(self, *args, **kwargs):
                        manager_cls.__init__(self, *args, **kwargs)

                    def __get__(self, instance, cls=None):
                        return manager_cls.__get__(instance, cls=cls)

                    def __getattr__(self, attr):
                        return getattr(manager_cls, attr)

                return DescriptorExt

        raise RuntimeError('could not determine the manager class from the'
                           'descriptor: %r' % self.descriptor)

    def __get__(self, instance, cls=None):
        if instance is None:
            return self
        return self.ext_class_final(instance)

    def __set__(self, instance, value):
        self.descriptor.__set__(instance, value)


class RelatedManagerExt:
    """
    Base class for implementing extensions for a related manager defined with
    the given `related_name`.
    """

    def __new__(cls, data):
        if isinstance(data, Model):
            new = object.__new__(cls)
            new.instance = data
            return new
        else:
            return RelatedDescriptorExt(data, cls)

    def __init__(self, instance):
        super().__init__(instance)


#
# Codeschool based models
#
class ShortDescriptionPageMixin(Model):
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

    content_panels = Page.content_panels + [
       _MultiFieldPanel([
           _FieldPanel('short_description'),
       ], heading=_('Options')),
    ]


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


#
# Patch wagtail's base Page model with extra methods from builtins
#
Page.__bases__ = (AbsoluteUrlMixin,) + Page.__bases__
Page.nav_sections = lambda self, request: []