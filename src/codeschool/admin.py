# flake8: noqa
from django.contrib.admin import site
from django.utils.translation import ugettext_lazy as _

from codeschool import mixins as _mixins
from codeschool import models as _models
from codeschool import panels as _panels
from codeschool.fixes.wagtailadmin import WagtailAdmin


class ShortDecriptionAdmin(WagtailAdmin):
    """
    Base admin class for all models that inherit from SHortPageDescription.
    """

    class Meta:
        model = _mixins.ShortDescriptionPage
        abstract = True

    content_panels = \
        _models.Page.content_panels + [
            _panels.MultiFieldPanel([
                _panels.FieldPanel('short_description'),
            ], heading=_('Options')),
        ]
