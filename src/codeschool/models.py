#
# One stop shop for models, fields and managers
#

# flake8: noqa
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
from model_utils.models import StatusModel, TimeFramedModel, TimeStampedModel
from model_utils.managers import QueryManager, InheritanceManager, QuerySet, InheritanceQuerySet

from .fixes.wagtailroutes import RoutableViewsPage
from .fixes.wagtailadmin import DecoupledAdminPage
from .managers import *
from .mixins import AbsoluteUrlMixin

#
# Patch wagtail's base Page model with extra methods from builtins
#
Page.__bases__ = (AbsoluteUrlMixin,) + Page.__bases__
Page.nav_sections = lambda self, request: []
